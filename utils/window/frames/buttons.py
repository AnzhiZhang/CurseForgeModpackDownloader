import os
from threading import Thread
from tkinter import Frame, Button, Toplevel
from tkinter.ttk import Combobox, Progressbar
from tkinter.messagebox import askokcancel
from tkinter.filedialog import askopenfilename
from typing import TYPE_CHECKING

from utils.constant import PATH
from utils.download import Download

if TYPE_CHECKING:
    from utils.window.main import Main


class Buttons(Frame):
    def __init__(self, master: 'Main'):
        super().__init__(master, height=50)

        self.__main_window = master

        self.__language_combobox = Combobox(self, state='readonly')
        self.__import_button = Button(
            self,
            text=self.__main_window.factory.language.translate(
                'window.buttons.import'
            ),
            background='white',
            command=lambda:
            Download(
                self.__main_window.factory,
                zip_file_path=askopenfilename()
            ).main()
        )
        self.__download_button = Button(
            self,
            text=self.__main_window.factory.language.translate(
                'window.buttons.download'
            ),
            background='white',
            command=self.download
        )
        self.__exit_button = Button(
            self,
            text=self.__main_window.factory.language.translate(
                'window.buttons.exit'
            ),
            background='white',
            command=master.quit
        )

        # Language
        self.__languages = {
            value: key for key, value in
            self.__main_window.factory.language.get_languages().items()
        }
        self.__language_combobox.bind(
            '<<ComboboxSelected>>',
            self.on_select_language
        )
        self.__language_combobox['values'] = list(self.__languages.keys())
        current_index = list(self.__languages.values()).index(
            self.__main_window.factory.config.get('language')
        )
        self.__language_combobox.current(current_index)

        self.__language_combobox.pack(side='left')
        self.__exit_button.pack(side='right')
        self.__download_button.pack(side='right', padx=10)
        self.__import_button.pack(side='right')

    def on_select_language(self, event=None) -> None:
        """
        Event handler for select a language.
        """
        language_key = self.__languages[self.__language_combobox.get()]
        if askokcancel(
                self.__main_window.factory.language.translate(
                    'window.buttons.languageSwitch.title',
                    lang=language_key
                ),
                self.__main_window.factory.language.translate(
                    'window.buttons.languageSwitch.content',
                    lang=language_key
                ),
        ):
            self.__main_window.factory.config['language'] = language_key
            self.__main_window.factory.config.save()
            self.__main_window.quit()

    def download(self) -> None:
        """
        Event handler for click download button.
        It will start to download a modpack.
        """
        def run():
            """
            Download modpack file.
            """
            # Progressbar
            toplevel = Toplevel(self)
            toplevel.title(
                self.__main_window.factory.language.translate(
                    'download.file.title'
                )
            )
            toplevel.resizable(False, False)
            toplevel.protocol("WM_DELETE_WINDOW", lambda: None)
            toplevel.iconbitmap(PATH.ICON_PATH)
            toplevel.focus_set()

            pb = Progressbar(toplevel, length=500)
            pb.pack(padx=10, pady=20)

            pb.start()

            # Download
            with open(file_path, 'wb') as f:
                f.write(
                    self.__main_window.factory.requester.get(
                        download_url
                    ).content
                )

            pb.stop()
            toplevel.destroy()

        # Disable button
        self.__download_button.configure(state='disabled')

        # Get info
        modpack_id = self.__main_window.show_frame.selected_modpack_id
        file_name = self.__main_window.show_frame.selected_file_name

        # Check selected
        if modpack_id != -1 and file_name != '':
            download_url = self.__main_window.show_frame.selected_download_url
            avatar_url = self.__main_window.show_frame.selected_avatar_url
            file_path = os.path.join(PATH.DOWNLOADING_DIR_PATH, file_name)

            if self.__main_window.factory.logger.debug_mode:
                self.__main_window.factory.logger.debug(
                    'Downloading modpack %s',
                    file_name
                )

            # Start download file
            thread = Thread(target=run, name='Download')
            thread.start()

            # Wait finish
            while thread.is_alive():
                self.update()

            # Other files
            Download(
                self.__main_window.factory,
                name=os.path.splitext(file_name)[0],
                zip_file_path=file_path,
                avatar_url=avatar_url
            ).main()

        # Enable button
        self.__download_button.configure(state='normal')
