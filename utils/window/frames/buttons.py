from tkinter import Frame, Button
from typing import TYPE_CHECKING

from utils.download import Download

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
            background='white'
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
