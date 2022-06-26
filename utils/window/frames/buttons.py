import os
from threading import Thread
from tkinter import Frame, Button, Toplevel
from tkinter.ttk import Progressbar
from tkinter.filedialog import askopenfilename
from typing import TYPE_CHECKING

from utils.constant import PATH
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
            command=lambda:
            Download(
                self.__main_window.factory.requester,
                zip_file_path=askopenfilename()
            ).main()
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
        def run():
            toplevel = Toplevel(self)
            toplevel.title('下载配置文件…………')
            toplevel.resizable(False, False)
            toplevel.protocol("WM_DELETE_WINDOW", lambda: None)
            toplevel.iconbitmap(PATH.ICON_PATH)
            toplevel.focus_set()

            pb = Progressbar(toplevel, length=500)
            pb.pack(padx=10, pady=20)

            pb.start()

            with open(file_path, 'wb') as f:
                f.write(
                    self.__main_window.factory.requester.get(
                        download_url
                    ).content
                )

            pb.stop()
            toplevel.destroy()

        # Disable button
        self.__download_button.configure(state='disabled')

        # Get info
        modpack_id = self.__main_window.show_frame.selected_modpack_id
        file_name = self.__main_window.show_frame.selected_file_name

        if modpack_id != -1 and file_name != '':
            download_url = self.__main_window.show_frame.selected_download_url
            avatar_url = self.__main_window.show_frame.selected_avatar_url
            file_path = os.path.join(PATH.TEMP_DIR_PATH, file_name)

            # Start download file
            thread = Thread(target=run, name='Download')
            thread.start()

            # Wait finish
            while thread.is_alive():
                self.update()

            # Other files
            Download(
                self.__main_window.factory.requester,
                name=os.path.splitext(file_name)[0],
                zip_file_path=file_path,
                avatar_url=avatar_url
            ).main()

        # Enable button
        self.__download_button.configure(state='normal')
