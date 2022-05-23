import os
import json
import shutil
import hashlib
from zipfile import ZipFile, ZIP_STORED
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo, showwarning

from utils.session import Session
from utils.logger import Logger

NAME = 'MinecraftModpackDownloader'


def unzip():
    with ZipFile(file_path) as zf:
        for i in zf.namelist():
            zf.extract(i, dir_path)


def get_download_urls():
    # 获取下载链接 API
    result = []
    with open(manifest_path) as f:
        data = json.load(f)
        files = data['files']
        count = len(files)
        for i, file in enumerate(files):
            logger.info(f'获取模组下载链接（{i + 1}/{count}）')
            result.append(
                session.get_download_url(file["projectID"], file["fileID"])
            )
    return result


def download_mods(urls):
    # 检查模组文件夹
    mods_dir_path = os.path.join(overrides_dir_path, 'mods')
    if not os.path.isdir(mods_dir_path):
        os.makedirs(mods_dir_path)

    # 下载模组
    count = len(urls)
    failed_mods = []
    for i, url in enumerate(urls):
        # 计算路径
        mod_name = os.path.basename(url)
        mods_path = os.path.join(mods_dir_path, mod_name)

        # 下载
        response = session.get(url)
        logger.info(f'下载模组（{i + 1}/{count}）：{mod_name}')

        # 校验
        md5 = hashlib.md5(response.content).hexdigest()
        if md5 != response.headers['ETag'].replace('"', ''):
            failed_mods.append(f'{mod_name}（{url}）')

        # 写入文件
        with open(mods_path, 'wb') as f:
            f.write(response.content)

    # 提示校验结果
    failed_count = len(failed_mods)
    if failed_count > 0:
        logger.info(f'{failed_count} 个模组校验失败\n' + '\n'.join(failed_mods))
        showwarning(
            '校验失败',
            f'{len(failed_mods)} 个模组校验失败，可能存在问题，请查看控制台获取详细信息'
        )


def write_mmc_files():
    # 获取版本信息
    with open(manifest_path) as f:
        data = json.load(f)['minecraft']
        minecraft_version = data['version']
        forge_version = data['modLoaders'][0]['id'].replace('forge-', '')

    # 写入 mmc-pack.json
    mmc_pack_path = os.path.join(dir_path, 'mmc-pack.json')
    with open(mmc_pack_path, 'w', encoding='utf-8') as f:
        json.dump({
            "components": [
                {
                    "uid": "net.minecraft",
                    "version": minecraft_version
                },
                {
                    "uid": "net.minecraftforge",
                    "version": forge_version
                }
            ],
            "formatVersion": 1
        }, f, indent=4)

    # 写入 instance.cfg
    instance_cfg_path = os.path.join(dir_path, 'instance.cfg')
    with open(instance_cfg_path, 'w', encoding='utf-8') as f:
        f.write('InstanceType=OneSix\n')


def clean_file():
    # 关闭日志
    logger.close()

    # 清理 CF 文件
    os.remove(manifest_path)
    os.remove(modlist_path)
    os.rename(overrides_dir_path, os.path.join(dir_path, '.minecraft'))

    # 压缩
    with ZipFile(file_path, mode='w', compression=ZIP_STORED) as zf:
        for dirpath, dirnames, filenames in os.walk(dir_path):
            for filename in filenames:
                zf_path = os.path.join(dirpath, filename)
                arcname = zf_path.replace(dir_path, dir_path.split(os.sep)[-1])
                zf.write(zf_path, arcname=arcname)

    # 删除文件夹
    shutil.rmtree(dir_path)


# 计算路径
file_path = askopenfilename().replace('/', os.sep)
if file_path == '':
    exit()
dir_path = file_path.replace('.zip', '')
log_file_path = os.path.join(dir_path, f'{NAME}.log')
overrides_dir_path = os.path.join(dir_path, 'overrides')
manifest_path = os.path.join(dir_path, 'manifest.json')
modlist_path = os.path.join(dir_path, 'modlist.html')

unzip()
logger = Logger(log_file_path)
session = Session()
download_urls = get_download_urls()
download_mods(download_urls)
write_mmc_files()
clean_file()
showinfo(
    '下载完成',
    '请直接导入启动器\n'
    '软件已开源，下载地址及问题反馈：\n'
    'https://github.com/AnzhiZhang/MinecraftModpackDownloader'
)
