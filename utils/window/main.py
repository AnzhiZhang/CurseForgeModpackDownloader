from tkinter import Tk
from ctypes import windll

from utils.constant import NAME_WITH_SPACE, WINDOW, PATH
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

        # High DPI
        # https://stackoverflow.com/questions/62794931/high-dpi-tkinter-re-scaling-when-i-run-it-in-spyder-and-when-i-run-it-direct-in
        windll.shcore.SetProcessDpiAwareness(2)
        scale_factor = windll.shcore.GetScaleFactorForDevice(0) / 75
        self.tk.call('tk', 'scaling', scale_factor)

        self.title_frame = frames.Title(self)
        self.search_frame = frames.Search(self)
        self.show_frame = frames.Show(self)
        self.filters_frame = frames.Filters(self)
        self.buttons_frame = frames.Buttons(self)

        self.title_frame.pack(**self.PACK_KWARGS)
        self.search_frame.pack(**self.PACK_KWARGS)
        self.show_frame.pack(**self.PACK_KWARGS, expand=True)
        self.filters_frame.pack(**self.PACK_KWARGS)
        self.buttons_frame.pack(**self.PACK_KWARGS)

        self.mainloop()


if __name__ == '__main__':
    Main()
