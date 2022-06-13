from tkinter import Frame, Entry, Label, Button


class Search(Frame):
    def __init__(self, master):
        super().__init__(master, height=50)

        self.search_entry = Entry(self)
        self.space1_label = Label(self, width=1)
        self.search_button = Button(self, text='搜索', background='white')

        self.search_entry.pack(side='left', fill='both', expand=True)
        self.space1_label.pack(side='left', fill='both')
        self.search_button.pack(side='left', fill='y')
