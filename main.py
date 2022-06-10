# 本文件是 CurseForgeModpackDownloader 的一部分。

# CurseForgeModpackDownloader 是自由软件：你可以再分发之和/或依照由自由软件基金会发布的 GNU 通用公共许可证修改之，无论是版本 3 许可证，还是（按你的决定）任何以后版都可以。

# 发布 CurseForgeModpackDownloader 是希望它能有用，但是并无保障；甚至连可销售和符合某个特定的目的都不保证。请参看 GNU 通用公共许可证，了解详情。

# 你应该随程序获得一份 GNU 通用公共许可证的复本。如果没有，请看 <https://www.gnu.org/licenses/>。
import os
import json
import shutil
import hashlib
from zipfile import ZipFile, ZIP_STORED
from concurrent.futures import ThreadPoolExecutor
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo, showwarning, askokcancel

from utils.requester import Requester
from utils.logger import Logger

NAME = 'CurseForgeModpackDownloader'


def unzip():
    with ZipFile(file_path) as zf:
        for i in zf.namelist():
            zf.extract(i, dir_path)


def get_download_urls():
    # 获取下载链接 API
    with open(manifest_path) as f:
        data = json.load(f)
        files = data['files']

    count = len(files)
    result = []
    i = 0
    for r in thread_pool.map(
            lambda file: Requester.download_url(
                file["projectID"],
                file["fileID"]
            ), files
    ):
        i += 1
        logger.info(f'获取模组下载链接（{i}/{count}）')
        result.append(r.text)
    return result


def download_mods(urls):
    def download(url):
        # 计算路径
        mod_name = os.path.basename(url)
        mod_path = os.path.join(mods_dir_path, mod_name)

        try:
            # 下载
            response = Requester.get(url)

            # 校验
            md5 = hashlib.md5(response.content).hexdigest()
            if md5 != response.headers['ETag'].replace('"', ''):
                failed_mods['verify'].append(f'{mod_name}（{url}）')

            # 写入文件
            with open(mod_path, 'wb') as f:
                f.write(response.content)
        except Exception as e:
            failed_mods['download'].append(f'{mod_name}（{url}）')
            logger.error(f'下载 {mod_name} 失败：{repr(e)}')

        return mod_name

    # 检查模组文件夹
    mods_dir_path = os.path.join(overrides_dir_path, 'mods')
    if not os.path.isdir(mods_dir_path):
        os.makedirs(mods_dir_path)

    # 下载模组
    count = len(urls)
    failed_mods = {
        'download': [],
        'verify': []
    }
    i = 0
    for name in thread_pool.map(download, urls):
        i += 1
        logger.info(f'下载模组（{i}/{count}）：{name}')

    # 提示结果
    warning_text = ''

    # 下载失败日志
    failed_download_count = len(failed_mods['download'])
    if failed_download_count > 0:
        warning_text += f'{failed_download_count} 个模组下载失败，请手动下载！\n'
        logger.error(
            f'{failed_download_count} 个模组下载失败，请手动下载：\n' +
            '\n'.join(failed_mods['download'])
        )

    # 验证失败日志
    failed_verify_count = len(failed_mods['verify'])
    if failed_verify_count > 0:
        warning_text += f'{failed_verify_count} 个模组校验失败，可能存在问题\n'
        logger.warning(
            f'{failed_verify_count} 个模组校验失败，一般无需手动下载：\n' +
            '\n'.join(failed_mods['verify'])
        )

    # 弹窗提示
    if warning_text:
        showwarning('警告', warning_text + '请查看控制台或日志获取详细信息')


def write_mmc_files():
    # 获取版本信息
    with open(manifest_path) as f:
        data = json.load(f)['minecraft']
        minecraft_version = data['version']
        mod_loader = data['modLoaders'][0]['id']
        if mod_loader.startswith('forge'):
            mod_loader_uid = 'net.minecraftforge'
        elif mod_loader.startswith('fabric'):
            mod_loader_uid = 'net.fabricmc.fabric-loader'
        mod_loader_version = mod_loader.split('-')[-1]

    # 写入 mmc-pack.json
    mmc_pack_path = os.path.join(dir_path, 'mmc-pack.json')
    with open(mmc_pack_path, 'w', encoding='utf-8') as f:
        json.dump({
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
        }, f, indent=4)

    # 写入 instance.cfg
    instance_cfg_path = os.path.join(dir_path, 'instance.cfg')
    with open(instance_cfg_path, 'w', encoding='utf-8') as f:
        f.write('InstanceType=OneSix\n')


def make_zip():
    # 清理 CF 文件
    modlist_path = os.path.join(dir_path, 'modlist.html')
    if os.path.isfile(modlist_path):
        os.remove(modlist_path)
    os.remove(manifest_path)
    os.rename(overrides_dir_path, os.path.join(dir_path, '.minecraft'))

    # 压缩
    with ZipFile(file_path, mode='w', compression=ZIP_STORED) as zf:
        for dirpath, dirnames, filenames in os.walk(dir_path):
            for filename in filenames:
                zf_path = os.path.join(dirpath, filename)
                arcname = zf_path.replace(dir_path, dir_path.split(os.sep)[-1])
                zf.write(zf_path, arcname=arcname)


def clean_file():
    # 关闭日志
    logger.close()

    # 删除文件夹
    shutil.rmtree(dir_path)


# 版权声明
accept = askokcancel(
    '版权声明',
    'Copyright © 2022 Andy Zhang\n'
    '本程序是自由软件：你可以再分发之和/或依照由自由软件基金会发布的 GNU 通用公共许可证修改之，无论是版本 3 许可证，还是（按你的决定）任何以后版都可以。\n'
    '发布该程序是希望它能有用，但是并无保障；甚至连可销售和符合某个特定的目的都不保证。请参看 GNU 通用公共许可证，了解详情。\n'
    '你应该随程序获得一份 GNU 通用公共许可证的复本。如果没有，请看 https://www.gnu.org/licenses/。'
)
if not accept:
    exit()

# 计算路径
file_path = askopenfilename().replace('/', os.sep)
if file_path == '':
    exit()
dir_path = file_path.replace('.zip', '')
log_file_path = os.path.join(dir_path, f'{NAME}.log')
overrides_dir_path = os.path.join(dir_path, 'overrides')
manifest_path = os.path.join(dir_path, 'manifest.json')

# 准备文件
unzip()

# 工具
logger = Logger(log_file_path)
thread_pool = ThreadPoolExecutor(4)

# 脚本
try:
    download_urls = get_download_urls()
except:
    clean_file()
    showwarning('警告', '获取模组下载地址失败，这可能是由于网络不稳定，请重试')
else:
    download_mods(download_urls)
    write_mmc_files()
    make_zip()
    clean_file()
    showinfo(
        '下载完成',
        '请直接导入启动器\n'
        '下载地址及问题反馈：\n'
        'https://github.com/AnzhiZhang/CurseForgeModpackDownloader'
    )
