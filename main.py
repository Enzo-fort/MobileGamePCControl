import os
import sys

from src.windows.main.main_app import MainApp

if sys.platform.lower() == "win32":
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        pass

if __name__ == "__main__":
    if getattr(sys, "frozen", False):
        os.chdir(os.path.dirname(sys.executable))
    else:
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
    MainApp()
