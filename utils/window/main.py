import sys
import platform
from tkinter import Tk
from tkinter.messagebox import askokcancel
from tkinter.simpledialog import askstring

from utils.constant import NAME_WITH_SPACE, WINDOW, PATH
from utils.factory import Factory
from utils.window import frames


class Main(Tk):
    PACK_KWARGS = {
        'fill': 'both',
        'padx': 15,
        'pady': 15
    }

    def __init__(self, factory: Factory):
        super().__init__()
        self.__factory = factory

        self.geometry(WINDOW.SIZE)
        self.minsize(WINDOW.WIDTH, WINDOW.HEIGHT)
        self.title(NAME_WITH_SPACE)
        self.iconbitmap(PATH.ICON_PATH)

        # High DPI on Windows
        # https://stackoverflow.com/questions/62794931/high-dpi-tkinter-re-scaling-when-i-run-it-in-spyder-and-when-i-run-it-direct-in
        if platform.system() == 'Windows':
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(2)
            scale_factor = windll.shcore.GetScaleFactorForDevice(0) / 75
            self.tk.call('tk', 'scaling', scale_factor)

        self.__title_frame = frames.Title(self)
        self.__search_frame = frames.Search(self)
        self.__show_frame = frames.Show(self)
        self.__filters_frame = frames.Filters(self)
        self.__buttons_frame = frames.Buttons(self)

        self.__title_frame.pack(**self.PACK_KWARGS)
        self.__search_frame.pack(**self.PACK_KWARGS)
        self.__show_frame.pack(**self.PACK_KWARGS, expand=True)
        self.__filters_frame.pack(**self.PACK_KWARGS)
        self.__buttons_frame.pack(**self.PACK_KWARGS)

    def main(self):
        # ask license
        if not (
                '--no-license' in sys.argv or
                askokcancel(
                    self.factory.language.translate('license.title'),
                    self.factory.language.translate('license.content')
                )
        ):
            return

        # ask api key
        if self.factory.config.get('curseForgeAPIKey') == '':
            result = askstring(
                'Configuration',
                '请输入 CurseForge API Key',
                show='*',
                parent=self
            )
            if result is None:
                self.quit()
            else:
                self.factory.requester.api_key = result
                self.factory.config['curseForgeAPIKey'] = result
                self.factory.config.save()

        # update list
        self.show_frame.update_list(force=True)

        # main loop
        self.mainloop()

    @property
    def factory(self):
        return self.__factory

    @property
    def search_frame(self):
        return self.__search_frame

    @property
    def show_frame(self):
        return self.__show_frame

    @property
    def filters_frame(self):
        return self.__filters_frame
