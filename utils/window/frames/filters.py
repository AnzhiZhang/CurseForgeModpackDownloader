from tkinter import Frame, Label
from tkinter.ttk import Combobox
from typing import TYPE_CHECKING, List

from utils.constant import SEARCH

if TYPE_CHECKING:
    from utils.window.main import Main


class Filters(Frame):
    def __init__(self, master: 'Main'):
        super().__init__(master, height=50)

        self.main_window = master

        self.sort_label = Label(self, text='排序方式：')
        self.sort_combobox = Combobox(self, state='readonly')
        self.game_version_label = Label(self, text='游戏版本：')
        self.game_version_combobox = Combobox(self, state='readonly')
        self.modpack_version_label = Label(self, text='整合包版本：')
        self.modpack_version_combobox = Combobox(self, state='readonly')

        self.sort_label.pack(side='left')
        self.sort_combobox.pack(side='left')
        self.game_version_label.pack(side='left', padx=(10, 0))
        self.game_version_combobox.pack(side='left')
        self.modpack_version_label.pack(side='left', padx=(10, 0))
        self.modpack_version_combobox.pack(side='left', fill='x', expand=True)

        # Set combobox values
        self.init()

    @property
    def sort(self):
        return self.sort_combobox.get()

    @property
    def game_version(self):
        return self.game_version_combobox.get()

    @property
    def modpack_version(self):
        return self.modpack_version_combobox.get()

    def init(self):
        self.sort_combobox['values'] = list(SEARCH.SORT.keys())
        self.sort_combobox.current(1)
        self.game_version_combobox['values'] = SEARCH.VERSIONS

    def set_modpack_version(self, values: List[str]):
        self.modpack_version_combobox['values'] = values
        self.modpack_version_combobox.current(0)
