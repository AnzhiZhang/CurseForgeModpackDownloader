import sys
from threading import Thread
# from ctypes import windll
from tkinter import Tk
from tkinter.messagebox import askokcancel

from utils.constant import NAME_WITH_SPACE, LICENSE, WINDOW, PATH
from utils.window import frames


class Main(Tk):
    PACK_KWARGS = {
        'fill': 'both',
        'padx': 15,
        'pady': 15
    }

    def __init__(self):
        super().__init__()
        self.geometry(WINDOW.SIZE)
        self.minsize(WINDOW.WIDTH, WINDOW.HEIGHT)
        self.title(NAME_WITH_SPACE)
        self.iconbitmap(PATH.ICON_PATH)

    # # High DPI
    # # https://stackoverflow.com/questions/62794931/high-dpi-tkinter-re-scaling-when-i-run-it-in-spyder-and-when-i-run-it-direct-in
    #    windll.shcore.SetProcessDpiAwareness(2)
    #    scale_factor = windll.shcore.GetScaleFactorForDevice(0) / 75
    #    self.tk.call('tk', 'scaling', scale_factor)

    #    self.__title_frame = frames.Title(self)
    #    self.__search_frame = frames.Search(self)
    #    self.__show_frame = frames.Show(self)
    #    self.__filters_frame = frames.Filters(self)
    #    self.__buttons_frame = frames.Buttons(self)

    #    self.__title_frame.pack(**self.PACK_KWARGS)
    #    self.__search_frame.pack(**self.PACK_KWARGS)
    #    self.__show_frame.pack(**self.PACK_KWARGS, expand=True)
    #    self.__filters_frame.pack(**self.PACK_KWARGS)
    #    self.__buttons_frame.pack(**self.PACK_KWARGS)

    #    Thread(target=self.__ask_license, name='Init').start()

    #    self.mainloop()
    #
    def __ask_license(self):
        """
        Ask to accept license.
        """
        if not ('--no-license' in sys.argv or askokcancel('版权声明', LICENSE)):
            self.quit()

    @property
    def search_frame(self):
        return self.__search_frame

    @property
    def show_frame(self):
        return self.__show_frame

    @property
    def filters_frame(self):
        return self.__filters_frame
