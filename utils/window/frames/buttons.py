import os
from tkinter import Frame, Button
from typing import TYPE_CHECKING

from utils.constant import PATH
from utils.download import Download
from utils.requester import Requester

if TYPE_CHECKING:
    from utils.window.main import Main


class Buttons(Frame):
    def __init__(self, master: 'Main'):
        super().__init__(master, height=50)

        self.__main_window = master

        self.__import_button = Button(
            self,
            text='导入',
            background='white',
            command=lambda: Download().main()
        )
        self.__download_button = Button(
            self,
            text='下载',
            background='white',
            command=self.download
        )
        self.__exit_button = Button(
            self,
            text='退出',
            background='white',
            command=master.quit
        )

        self.__exit_button.pack(side='right')
        self.__download_button.pack(side='right', padx=10)
        self.__import_button.pack(side='right')

    def download(self):
        modpack_id = self.__main_window.show_frame.selected_modpack_id
        file_name = self.__main_window.show_frame.selected_file_name

        if modpack_id != -1 and file_name != '':
            download_url = self.__main_window.show_frame.selected_download_url
            avatar_url = self.__main_window.show_frame.selected_avatar_url

            file_path = os.path.join(os.getcwd(), PATH.TEMP_DIR_PATH, file_name)
            with open(file_path, 'wb') as f:
                f.write(Requester.get(download_url).content)
            Download(
                name=os.path.splitext(file_name)[0],
                zip_file_path=file_path,
                avatar_url=avatar_url
            ).main()
