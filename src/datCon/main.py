import customtkinter as ctk
from classes import *
from views import *


class DatConApp(ctk.CTk):
    """The main application class for datCon."""

    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.resizable(0, 0)
        self.title("datCon")
        self.iconbitmap("Assets/datCon.ico")
        self.current_blade = Blade()
        main_view(self)


if __name__ == "__main__":
    app = DatConApp()
    app.mainloop()


def Exit():
    app.destroy()
    exit()
