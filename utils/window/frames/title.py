from tkinter import Frame, Label

from utils.constant import NAME_WITH_SPACE


class Title(Frame):
    def __init__(self, master):
        super().__init__(master, height=50)

        Label(self, text=NAME_WITH_SPACE, font=('Arial', 12)).pack(side='left')
