import os
import sys
import shutil
from tkinter.messagebox import askokcancel

from utils.constant import PATH
from utils.download import Download


def main():
    # 清理临时文件夹
    if os.path.isdir(PATH.TEMP_DIR_PATH):
        shutil.rmtree(PATH.TEMP_DIR_PATH)
    os.mkdir(PATH.TEMP_DIR_PATH)

    # 版权声明
    if '--no-license' not in sys.argv:
        accept = askokcancel(
            '版权声明',
            'Copyright © 2022 Andy Zhang\n'
            '本程序是自由软件：你可以再分发之和/或依照由自由软件基金会发布的 GNU 通用公共许可证修改之，无论是版本 3 许可证，还是（按你的决定）任何以后版都可以。\n'
            '发布该程序是希望它能有用，但是并无保障；甚至连可销售和符合某个特定的目的都不保证。请参看 GNU 通用公共许可证，了解详情。\n'
            '你应该随程序获得一份 GNU 通用公共许可证的复本。如果没有，请看 https://www.gnu.org/licenses/。'
        )
        if not accept:
            exit()

    Download().main()

    shutil.rmtree(PATH.TEMP_DIR_PATH)


if __name__ == '__main__':
    main()
