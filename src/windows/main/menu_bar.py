from tkinter import Menu, messagebox


class MenuBar:
    def __init__(self, parent):
        self.parent = parent
        menu = Menu(parent)
        parent.config(menu=menu)
        settings = Menu(menu, tearoff=0)
        settings.add_command(label="Reset to Defaults", command=parent.reset_settings)
        settings.add_separator()
        settings.add_command(label="Exit", command=parent.quit_software)
        menu.add_cascade(label="Settings", menu=settings)
        help_menu = Menu(menu, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu.add_cascade(label="Help", menu=help_menu)

    def show_about(self):
        messagebox.showinfo("About MobileGamePCControl", "MobileGamePCControl\n\nConfigurable keyboard-to-mouse control.")
