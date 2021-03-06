from threading import Thread
from tkinter import Frame, Listbox, Scrollbar
from tkinter.messagebox import showwarning
from typing import TYPE_CHECKING, List, Dict

from utils.constant import SEARCH

if TYPE_CHECKING:
    from utils.window.main import Main


class Show(Frame):
    def __init__(self, master: 'Main'):
        super().__init__(master)

        self.__main_window = master
        self.__search_index = -1
        self.__selected_index = -1
        self.__updating = True
        self.__data: List[Dict] = []

        self.__list_listbox = Listbox(self, font=('Arial', 12))
        self.__list_listbox_scrollbar = Scrollbar(self)

        # Scrollbar setting
        self.__list_listbox.config(yscrollcommand=self.__on_scroll)
        self.__list_listbox_scrollbar.config(command=self.__list_listbox.yview)

        self.__list_listbox.bind("<<ListboxSelect>>", self.__on_listbox_select)

        self.__list_listbox.pack(side='left', fill='both', expand=True)
        self.__list_listbox_scrollbar.pack(side='left', fill='y')

    def update_list(self, append=False, force=False) -> None:
        """
        Get filters and search modpacks, then update the list.
        :param append: Append new modpacks to end.
        :param force: It will ignore list is updating if it is True.
        """

        def request(index: int) -> dict:
            """
            Get filters and search modpacks from API.
            :param index: Search index.
            :return: API requested result.
            """
            # Get filters
            keyword = sorting = game_version = None
            if self.__main_window.search_frame.keyword:
                keyword = self.__main_window.search_frame.keyword
            if self.__main_window.filters_frame.sort:
                sorting = SEARCH.SORTING[self.__main_window.filters_frame.sort]
            if self.__main_window.filters_frame.game_version:
                game_version = self.__main_window.filters_frame.game_version

            return self.__main_window.factory.requester.search_modpack(
                game_version=game_version,
                search_filter=keyword,
                sorting=sorting,
                index=index
            ).json()

        def run() -> None:
            self.__updating = True

            # Refresh list or append
            if not append:
                self.__search_index = 0
                self.__selected_index = -1
                self.__data = []
                self.__list_listbox.delete(0, 'end')
            else:
                self.__search_index += 1

            # Request and check result
            result = request(self.__search_index)['data']
            if len(result) == 0:
                showwarning(
                    self.__main_window.factory.language.translate(
                        'window.show.resultWarning.title'
                    ),
                    self.__main_window.factory.language.translate(
                        'window.show.resultWarning.content'
                    )
                )

            # Add request results
            for i in result:
                self.__data.append(i)
                self.__list_listbox.insert('end', i['name'].strip())

            # Clean modpack version filter
            self.__main_window.filters_frame.set_modpack_version([''])

            self.__updating = False

        # Protection
        if force or not self.__updating:
            Thread(
                target=run,
                name='Update List Data'
            ).start()

    def __on_scroll(self, first: float, last: float) -> None:
        """
        List scroll event, to search and append more modpacks to the end.
        :param first: Top of listbox in percentage, provided from tkinter.
        :param last: Bottom of listbox in percentage, provided from tkinter.
        """
        # Call origin function
        self.__list_listbox_scrollbar.set(first, last)

        # Update at the end
        if float(last) == 1.0 and not self.__updating:
            self.update_list(append=True)

    def __on_listbox_select(self, event=None) -> None:
        """
        Event handler of listbox selected to update modpack versions.
        """
        def run():
            # Clean filter combobox
            self.__main_window.filters_frame.set_modpack_version([''])

            # Get files
            files = self.__main_window.factory.requester.files(
                project_id
            ).json()['data']

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
                project_id = self.__data[self.selected_index].get('id')
                Thread(
                    target=run,
                    name=f'Get Modpack Files ({project_id})'
                ).start()

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
            selected_file_id = self.selected_files[display_name]['id']
            return 'https://edge.forgecdn.net/files/{}/{}/{}'.format(
                int(selected_file_id / 1000),
                selected_file_id % 1000,
                self.selected_file_name
            )
        return ''

    @property
    def selected_avatar_url(self) -> str:
        display_name = self.__main_window.filters_frame.modpack_version
        if display_name != '' and self.selected_files is not None:
            return self.__data[self.selected_index]['logo']['url']
        return ''

    def reselect(self) -> None:
        """
        Reselect item in list.
        """
        self.__list_listbox.select_set(self.selected_index)
