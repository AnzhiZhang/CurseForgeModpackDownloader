from tkinter import Frame, Button

from utils.download import Download


class Buttons(Frame):
    def __init__(self, master):
        super().__init__(master, height=50)

        self.import_button = Button(
            self,
            text='导入',
            background='white',
            command=lambda: Download().main()
        )
        self.download_button = Button(
            self,
            text='下载',
            background='white'
        )
        self.exit_button = Button(
            self,
            text='退出',
            background='white',
            command=master.quit
        )

        self.exit_button.pack(side='right')
        self.download_button.pack(side='right', padx=10)
        self.import_button.pack(side='right')
