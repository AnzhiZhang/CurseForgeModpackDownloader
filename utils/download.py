import os
import sys
import json
import shutil
import hashlib
from threading import Thread
from zipfile import ZipFile, ZIP_STORED
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING, Callable
from tkinter import Toplevel
from tkinter.ttk import Progressbar
from tkinter.messagebox import showinfo, showwarning

from utils.constant import NAME, PATH
from utils.logger import Logger

if TYPE_CHECKING:
    from utils.factory import Factory


class Download:
    def __init__(
            self,
            factory: 'Factory',
            name: str = None,
            zip_file_path: str = None,
            avatar_url: str = None
    ):
        self.factory = factory
        self.requester = self.factory.requester
        self.name = name
        self.zip_file_path = zip_file_path
        self.avatar_url = avatar_url
        self.avatar_name = None
        self.avatar_path = None

        self.dir_path = None
        self.log_file_path = None
        self.overrides_dir_path = None
        self.manifest_path = None
        self.logger = None
        self.thread_pool = None

    def main(self):
        # 处理名称
        if not self.name:
            self.name = os.path.basename(self.zip_file_path)
        self.name = self.name.strip()

        # 计算路径
        self.dir_path = os.path.join(PATH.DOWNLOADING_DIR_PATH, self.name)
        self.log_file_path = os.path.join(self.dir_path, f'{NAME}.log')
        self.overrides_dir_path = os.path.join(self.dir_path, 'overrides')
        self.manifest_path = os.path.join(self.dir_path, 'manifest.json')

        # 处理图标名称
        if self.avatar_url:
            ext = os.path.splitext(os.path.basename(self.avatar_url))[1]
            self.avatar_name = self.name.replace(' ', '_').replace('.', '_')
            self.avatar_path = os.path.join(
                self.dir_path,
                self.avatar_name + ext
            )

        # 新建临时文件夹
        os.mkdir(self.dir_path)
        if self.factory.logger.debug_mode:
            self.factory.logger.debug(
                'Successfully created temp dir %s for modpack %s',
                self.dir_path,
                self.name
            )

        # 工具
        self.logger = Logger(self.name, self.log_file_path)
        self.thread_pool = ThreadPoolExecutor(4)

        if '--debug' in sys.argv:
            self.logger.set_debug(True)

        def run():
            toplevel = Toplevel()
            toplevel.title(
                self.factory.language.translate('download.mods.title')
            )
            toplevel.resizable(False, False)
            toplevel.protocol("WM_DELETE_WINDOW", lambda: None)
            toplevel.iconbitmap(PATH.ICON_PATH)
            toplevel.focus_set()

            pb = Progressbar(toplevel, length=500, mode='determinate')
            pb.pack(padx=10, pady=20)

            # 解压文件
            self.unzip()
            self.logger.info(
                self.factory.language.translate('download.logging.unzipped')
            )

            # 设置进度条
            pb['maximum'] = self.mod_count * 2
            pb['value'] = 0

            def update():
                """
                Update progressbar.
                """
                pb['value'] = pb['value'] + 1
                toplevel.update()

            def clear():
                """
                Clear file and destroy progressbar.
                """
                self.clear_file()
                toplevel.destroy()

            try:
                # 下载图标
                if self.avatar_url:
                    with open(self.avatar_path, 'wb') as f:
                        f.write(self.requester.get(self.avatar_url).content)
                    if self.logger.debug_mode:
                        self.logger.debug(
                            'Downloaded avatar from %s and saved to %s',
                            self.avatar_url,
                            self.avatar_path
                        )

                # 获取模组下载链接
                download_urls = self.get_download_urls(update)
            except Exception as e:
                self.logger.exception(f'Exception: {e}')
                clear()
                showwarning(
                    self.factory.language.translate(
                        'download.getURLFail.title'
                    ),
                    self.factory.language.translate(
                        'download.getURLFail.content'
                    )
                )
            else:
                self.download_mods(download_urls, update)
                self.write_mmc_files()
                self.make_zip()
                clear()
                showinfo(
                    self.factory.language.translate('download.finish.title'),
                    self.factory.language.translate('download.finish.content')
                )
                self.factory.logger.info(
                    self.factory.language.translate(
                        'download.logging.success',
                        self.name
                    )
                )

        Thread(target=run, name='Download').start()

    @property
    def mod_count(self):
        with open(self.manifest_path) as f:
            return len(json.load(f)['files'])

    def unzip(self):
        with ZipFile(self.zip_file_path) as zf:
            for i in zf.namelist():
                zf.extract(i, self.dir_path)

    def get_download_urls(self, update: Callable):
        with open(self.manifest_path) as f:
            data = json.load(f)
            files = data['files']

        count = len(files)
        self.logger.info(
            self.factory.language.translate('download.logging.foundMods', count)
        )
        result = []
        i = 0
        for r in self.thread_pool.map(
                lambda file: self.requester.get_mod_file(
                    file['projectID'],
                    file['fileID']
                ), files
        ):
            i += 1
            update()
            data = r.json()['data']
            url = 'https://edge.forgecdn.net/files/{}/{}/{}'.format(
                int(data['id'] / 1000),
                data['id'] % 1000,
                data['fileName']
            )
            result.append(url)
            self.logger.info(
                self.factory.language.translate(
                    'download.logging.gotDownloadURL',
                    i, count, url
                )
            )
        return result

    def download_mods(self, urls, update: Callable):
        def download(url):
            # 计算路径
            mod_name = os.path.basename(url)
            mod_path = os.path.join(mods_dir_path, mod_name)

            try:
                # 下载
                response = self.requester.get(url)

                # 校验
                calculated_md5 = hashlib.md5(response.content).hexdigest()
                server_md5 = response.headers['ETag'].replace('"', '')
                if calculated_md5 != server_md5:
                    failed_mods['verify'].append(f'{mod_name}（{url}）')
                    if self.logger.debug_mode:
                        self.logger.debug(
                            'Mod %s\'s calculated md5 value %s '
                            'is difference with server provided md5 value %s!',
                            mod_name,
                            calculated_md5,
                            server_md5
                        )

                # 写入文件
                with open(mod_path, 'wb') as f:
                    f.write(response.content)
            except Exception as e:
                failed_mods['download'].append(f'{mod_name}（{url}）')
                self.logger.error(f'下载 {mod_name} 失败：{repr(e)}')

            return mod_name

        # 检查模组文件夹
        mods_dir_path = os.path.join(self.overrides_dir_path, 'mods')
        if not os.path.isdir(mods_dir_path):
            os.makedirs(mods_dir_path)

        # 下载模组
        count = len(urls)
        failed_mods = {
            'download': [],
            'verify': []
        }
        i = 0
        for name in self.thread_pool.map(download, urls):
            i += 1
            update()
            self.logger.info(
                self.factory.language.translate(
                    'download.logging.gotMod',
                    i, count, name
                )
            )

        # 提示结果
        warning_text = ''

        # 下载失败日志
        failed_download_count = len(failed_mods['download'])
        if failed_download_count > 0:
            warning_text += self.factory.language.translate(
                'download.downloadFail',
                failed_download_count
            )
            self.logger.error(
                self.factory.language.translate(
                    'download.logging.downloadFail',
                    failed_download_count, '\n'.join(failed_mods['download'])
                )
            )

        # 验证失败日志
        failed_verify_count = len(failed_mods['verify'])
        if failed_verify_count > 0:
            self.logger.warning(
                self.factory.language.translate(
                    'download.logging.verifyFail',
                    failed_verify_count, '\n'.join(failed_mods['verify'])
                )
            )

        # 弹窗提示
        if warning_text != '':
            showwarning(
                self.factory.language.translate('download.getModWarning.title'),
                self.factory.language.translate(
                    'download.getModWarning.content',
                    warning_text
                ),
            )

    def write_mmc_files(self):
        # 获取版本信息
        with open(self.manifest_path) as f:
            data = json.load(f)['minecraft']
            minecraft_version = data['version']
            mod_loader = data['modLoaders'][0]['id']
            if mod_loader.startswith('forge'):
                mod_loader_uid = 'net.minecraftforge'
            elif mod_loader.startswith('fabric'):
                mod_loader_uid = 'net.fabricmc.fabric-loader'
            mod_loader_version = mod_loader.split('-')[-1]

        # 写入 mmc-pack.json
        mmc_pack_path = os.path.join(self.dir_path, 'mmc-pack.json')
        data = {
            'components': [
                {
                    'uid': 'net.minecraft',
                    'version': minecraft_version
                },
                {
                    'uid': mod_loader_uid,
                    'version': mod_loader_version
                }
            ],
            'formatVersion': 1
        }
        with open(mmc_pack_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        if self.logger.debug_mode:
            self.logger.debug(
                'Saved following data into %s:\n%s',
                mmc_pack_path,
                data
            )

        # 写入 instance.cfg
        instance_cfg_path = os.path.join(self.dir_path, 'instance.cfg')
        content = 'InstanceType=OneSix\n'
        if self.avatar_url:
            content += f'iconKey={self.avatar_name}\n'
        with open(instance_cfg_path, 'w', encoding='utf-8') as f:
            f.write(content)
        if self.logger.debug_mode:
            self.logger.debug(
                'Saved following data into %s:\n%s',
                instance_cfg_path,
                content
            )

    def make_zip(self):
        # 清理 CF 文件
        modlist_path = os.path.join(self.dir_path, 'modlist.html')
        if os.path.isfile(modlist_path):
            os.remove(modlist_path)
            if self.logger.debug_mode:
                self.logger.debug('Deleted file %s', modlist_path)
        os.remove(self.manifest_path)
        if self.logger.debug_mode:
            self.logger.debug('Deleted file %s', self.manifest_path)
        os.rename(
            self.overrides_dir_path,
            os.path.join(self.dir_path, '.minecraft')
        )
        if self.logger.debug_mode:
            self.logger.debug('Renamed overrides to .minecraft')

        # 压缩
        with ZipFile(self.zip_file_path, mode='w', compression=ZIP_STORED) as z:
            for dirpath, dirnames, filenames in os.walk(self.dir_path):
                for filename in filenames:
                    zf_path = os.path.join(dirpath, filename)
                    arcname = zf_path.replace(
                        self.dir_path,
                        self.dir_path.split(os.sep)[-1]
                    )
                    z.write(zf_path, arcname=arcname)
        if self.logger.debug_mode:
            self.logger.debug('Made zip %s', self.zip_file_path)

        # Move to out of temp dir
        if PATH.DOWNLOADING_DIR_PATH in self.zip_file_path:
            shutil.move(self.zip_file_path, '.')

    def clear_file(self):
        # 关闭日志
        self.logger.close()

        # 删除文件夹
        shutil.rmtree(self.dir_path)
