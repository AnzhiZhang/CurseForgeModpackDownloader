from tkinter import Frame, Label
from tkinter.ttk import Combobox


class Filters(Frame):
    def __init__(self, master):
        super().__init__(master, height=50)

        self.sort_label = Label(self, text='排序方式：')
        self.sort_combobox = Combobox(self)
        self.game_version_label = Label(self, text='游戏版本：')
        self.game_version_combobox = Combobox(self)
        self.modpack_version_label = Label(self, text='整合包版本：')
        self.modpack_version_combobox = Combobox(self)

        self.sort_label.pack(side='left')
        self.sort_combobox.pack(side='left')
        self.game_version_label.pack(side='left', padx=(10, 0))
        self.game_version_combobox.pack(side='left')
        self.modpack_version_label.pack(side='left', padx=(10, 0))
        self.modpack_version_combobox.pack(side='left')
