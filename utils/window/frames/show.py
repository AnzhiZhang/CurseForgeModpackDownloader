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

        self.__main_window = master
        self.__search_index = 0
        self.__selected_index = -1
        self.__updating = False
        self.__data: List[Dict] = []

        self.__list_listbox = Listbox(self, font=('Arial', 12))
        self.__list_listbox_scrollbar = Scrollbar(self)

        # Scrollbar setting
        self.__list_listbox.config(yscrollcommand=self.__on_scroll)
        self.__list_listbox_scrollbar.config(command=self.__list_listbox.yview)

        self.__list_listbox.bind("<<ListboxSelect>>", self.__on_listbox_select)

        self.__list_listbox.pack(side='left', fill='both', expand=True)
        self.__list_listbox_scrollbar.pack(side='left', fill='y')

    def update_list(self, append=False):
        def request(index):
            # Get filters
            keyword = sort = game_version = None
            if self.__main_window.search_frame.keyword:
                keyword = self.__main_window.search_frame.keyword
            if self.__main_window.filters_frame.sort:
                sort = SEARCH.SORT[self.__main_window.filters_frame.sort]
            if self.__main_window.filters_frame.game_version:
                game_version = self.__main_window.filters_frame.game_version

            return Requester.search_modpack(
                game_version=game_version,
                search_filter=keyword,
                sort=sort,
                index=index
            ).json()

        def run():
            self.__updating = True

            # Refresh list or append
            if not append:
                self.__selected_index = -1
                self.__data = []
                self.__list_listbox.delete(0, 'end')
            else:
                self.__search_index += 1

            # Add request results
            for i in request(self.__search_index):
                self.__data.append(i)
                self.__list_listbox.insert('end', i['name'].strip())

            # Clean modpack version filter
            self.__main_window.filters_frame.set_modpack_version([''])

            self.__updating = False

        # Protection
        if not self.__updating:
            Thread(
                target=run,
                name='Update List Data'
            ).start()

    def __on_scroll(self, first, last):
        # Call origin function
        self.__list_listbox_scrollbar.set(first, last)

        # Update at the end
        if float(last) == 1.0 and not self.__updating:
            self.update_list(append=True)

    def __on_listbox_select(self, event=None):
        def run():
            # Clean filter combobox
            self.__main_window.filters_frame.set_modpack_version([''])

            # Get files
            files = Requester.files(_id).json()

            # Storage into data
            self.__data[self.selected_index]['files'] = {}
            for i in files:
                display_name = i['displayName']
                self.__data[self.selected_index]['files'][display_name] = i

            # Set filter combobox
            self.__main_window.filters_frame.set_modpack_version(
                list(self.__data[self.selected_index]['files'].keys())
            )

        old_index = self.selected_index

        selection = self.__list_listbox.curselection()
        if selection:
            self.__selected_index = selection[0]
            if self.selected_index == old_index:
                return
            else:
                _id = self.__data[self.selected_index].get('id')
                Thread(target=run, name=f'Get Modpack Versions ({_id})').start()

    @property
    def selected_index(self) -> int:
        return self.__selected_index

    @property
    def selected_modpack_id(self) -> int:
        index = self.selected_index
        return self.__data[index].get('id') if index != -1 else -1

    @property
    def selected_files(self) -> Dict:
        if self.selected_index != -1:
            return self.__data[self.selected_index].get('files')

    @property
    def selected_file_name(self) -> str:
        display_name = self.__main_window.filters_frame.modpack_version
        if display_name != '' and self.selected_files is not None:
            return self.selected_files[display_name]['fileName']
        return ''

    @property
    def selected_download_url(self) -> str:
        display_name = self.__main_window.filters_frame.modpack_version
        if display_name != '' and self.selected_files is not None:
            return self.selected_files[display_name]['downloadUrl']
        return ''

    @property
    def selected_avatar_url(self) -> str:
        display_name = self.__main_window.filters_frame.modpack_version
        if display_name != '' and self.selected_files is not None:
            return self.__data[self.selected_index]['attachments'][0]['url']
        return ''

    def reselect(self):
        """
        Reselect item in list.
        """
        self.__list_listbox.select_set(self.selected_index)
