import os
import json
import shutil
import time
import webbrowser
import zipfile
from zipfile import ZipFile

from lxml import html


def unzip():
    with ZipFile(file_path) as zf:
        for i in zf.namelist():
            zf.extract(i, dir_path)


def get_combine_download_urls():
    def get_file_ids():
        with open(manifest_path) as f:
            data = json.load(f)
            return [i['fileID'] for i in data['files']]

    def get_mod_urls():
        root = html.parse(modlist_path)
        return root.xpath('//li/a/@href')

    file_ids = get_file_ids()
    mod_urls = get_mod_urls()

    result = []
    for i in range(len(file_ids)):
        result.append(f'{mod_urls[i]}/download/{file_ids[i]}/file')
    return result


def download_mods(urls):
    mods_path = os.path.join(overrides_dir_path, 'mods')
    if not os.path.isdir(mods_path):
        os.makedirs(mods_path)
    print(urls)
    for i in urls:
        webbrowser.open(i)
        time.sleep(0.2)


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
    # 清理 CF 文件
    os.remove(manifest_path)
    os.remove(modlist_path)
    os.rename(overrides_dir_path, os.path.join(dir_path, '.minecraft'))

    # 压缩
    with ZipFile(file_path, mode='w', compression=zipfile.ZIP_STORED) as zf:
        for dirpath, dirnames, filenames in os.walk(dir_path):
            for filename in filenames:
                zf_path = os.path.join(dirpath, filename)
                arcname = zf_path.replace(dir_path, dir_path.split(os.sep)[-1])
                zf.write(zf_path, arcname=arcname)

    # 删除文件夹
    shutil.rmtree(dir_path)


# 计算路径
file_path = input('文件路径：')
dir_path = file_path.replace('.zip', '')
overrides_dir_path = os.path.join(dir_path, 'overrides')
manifest_path = os.path.join(dir_path, 'manifest.json')
modlist_path = os.path.join(dir_path, 'modlist.html')

unzip()
download_urls = get_combine_download_urls()
print(f'开始下载 {len(download_urls)} 个模组')
download_mods(download_urls)
input('请下载完成后手动移动文件，然后按回车继续')
write_mmc_files()
clean_file()
