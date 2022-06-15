from threading import Thread
from tkinter import Frame, Listbox, Scrollbar
from typing import TYPE_CHECKING, List, Dict

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
        self.data: List[Dict] = []

        self.list_listbox = Listbox(self, font=('Arial', 12))
        self.list_listbox_scrollbar = Scrollbar(self)

        # Scrollbar setting
        self.list_listbox.config(yscrollcommand=self.on_scroll)
        self.list_listbox_scrollbar.config(command=self.list_listbox.yview)

        self.list_listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

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
                self.data = []
                self.list_listbox.delete(0, 'end')
            else:
                self.index += 1

            # Add request results
            for i in request(self.index):
                self.data.append(i)
                self.list_listbox.insert('end', i['name'].strip())

            # Clean modpack version filter
            self.main_window.filters_frame.set_modpack_version([''])

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

    def on_listbox_select(self, event=None):
        def run():
            files = Requester.files(_id).json()

            # Storage into data
            self.data[index]['files'] = {}
            for i in files:
                self.data[index]['files'][i['displayName']] = i

            # Set filter combobox
            self.main_window.filters_frame.set_modpack_version(
                list(self.data[index]['files'].keys())
            )

        selection = self.list_listbox.curselection()
        if selection:
            index = selection[0]
            _id = self.data[index].get('id')
            Thread(target=run, name=f'Get Modpack Versions ({_id})').start()
