from threading import Thread
from tkinter import Frame, Listbox, Scrollbar
from typing import TYPE_CHECKING

from utils.constant import SEARCH
from utils.requester import Requester

if TYPE_CHECKING:
    from utils.window.main import Main


class Show(Frame):
    def __init__(self, master: 'Main'):
        super().__init__(master)

        self.main_window = master
        self.index = 0
        self.updating = False

        self.list_listbox = Listbox(self, font=('Arial', 12))
        self.list_listbox_scrollbar = Scrollbar(self)

        # Scrollbar setting
        self.list_listbox.config(yscrollcommand=self.on_scroll)
        self.list_listbox_scrollbar.config(command=self.list_listbox.yview)

        self.list_listbox.pack(side='left', fill='both', expand=True)
        self.list_listbox_scrollbar.pack(side='left', fill='y')

    def update_list(self, append=False):
        def request(index):
            # Get filters
            keyword = sort = game_version = None
            if self.main_window.search_frame.keyword:
                keyword = self.main_window.search_frame.keyword
            if self.main_window.filters_frame.sort:
                sort = SEARCH.SORT[self.main_window.filters_frame.sort]
            if self.main_window.filters_frame.game_version:
                game_version = self.main_window.filters_frame.game_version

            return Requester.search_modpack(
                game_version=game_version,
                search_filter=keyword,
                sort=sort,
                index=index
            ).json()

        def run():
            self.updating = True

            # Refresh list or append
            if not append:
                self.list_listbox.delete(0, 'end')
            else:
                self.index += 1

            # Add request results
            for i in request(self.index):
                self.list_listbox.insert('end', i['name'].strip())

            self.updating = False

        # Protection
        if not self.updating:
            Thread(
                target=run,
                name='Update List Data'
            ).start()

    def on_scroll(self, first, last):
        # Call origin function
        self.list_listbox_scrollbar.set(first, last)

        # Update at the end
        if float(last) == 1.0 and not self.updating:
            self.update_list(append=True)
