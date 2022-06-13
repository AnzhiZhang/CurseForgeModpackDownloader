from tkinter import Frame, Listbox


class Show(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.list_listbox = Listbox(self, font=('Arial', 12))

        self.list_listbox.pack(fill='both', expand=True)
