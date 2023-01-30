import customtkinter as ctk
from classes import *
from views import *


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # set appearance mode and default color theme
        # Modes: "System" (standard), "Dark", "Light"
        ctk.set_appearance_mode("System")
        # Themes: "blue" (standard), "green", "dark-blue"
        ctk.set_default_color_theme("blue")
        self.resizable(0, 0)
        # self.geometry("1000x600")
        self.title("datCon")
        self.iconbitmap("Assets/datCon.ico")
        # initialize an empty blade object
        self.current_blade = Blade()
        # initialize the window
        main_view(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
