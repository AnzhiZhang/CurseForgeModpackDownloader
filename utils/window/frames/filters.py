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

        self.sort_label = Label(
            self,
            text=self.main_window.factory.language.translate(
                'window.filters.sort'
            )
        )
        self.sort_combobox = Combobox(self, width=15, state='readonly')
        self.game_version_label = Label(
            self,
            text=self.main_window.factory.language.translate(
                'window.filters.gameVersion'
            )
        )
        self.game_version_combobox = Combobox(self, width=10, state='readonly')
        self.modpack_version_label = Label(
            self,
            text=self.main_window.factory.language.translate(
                'window.filters.modpackVersion'
            )
        )
        self.modpack_version_combobox = Combobox(self, state='readonly')

        # Update list when combobox selected
        self.sort_combobox.bind('<<ComboboxSelected>>', self.on_select)
        self.game_version_combobox.bind('<<ComboboxSelected>>', self.on_select)
        self.modpack_version_combobox.bind(
            '<<ComboboxSelected>>',
            self.on_modpack_version_select
        )

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

    def init(self) -> None:
        """
        Set values of comboboxex.
        """
        self.sort_combobox['values'] = list(SEARCH.SORTING.keys())
        self.sort_combobox.current(1)
        self.game_version_combobox['values'] = SEARCH.VERSIONS

    def set_modpack_version(self, values: List[str]) -> None:
        """
        Function to update modpack version combobox.
        :param values: A string list contains all values.
        """
        self.modpack_version_combobox['values'] = values
        self.modpack_version_combobox.current(0)

    def on_select(self, event=None) -> None:
        """
        Select a filter event handler. It will update nodpack list.
        """
        self.main_window.show_frame.update_list()

    def on_modpack_version_select(self, event=None) -> None:
        """
        Select a modpack version filter handler.
        """
        self.main_window.show_frame.reselect()
