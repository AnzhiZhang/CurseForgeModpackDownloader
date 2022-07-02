from tkinter import Frame, Entry, Button
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.window.main import Main


class Search(Frame):
    def __init__(self, master: 'Main'):
        super().__init__(master, height=50)

        self.main_window = master

        self.search_entry = Entry(self)
        self.search_button = Button(
            self,
            text=self.main_window.factory.language.translate(
                'window.search.search'
            ),
            background='white',
            command=self.on_search
        )

        # Allow press enter in entry to search
        self.search_entry.bind('<Return>', self.on_search)

        self.search_entry.pack(side='left', fill='both', expand=True)
        self.search_button.pack(side='left', fill='y', padx=(10, 0))

    @property
    def keyword(self):
        return self.search_entry.get()

    def on_search(self, event=None):
        self.main_window.show_frame.update_list()
