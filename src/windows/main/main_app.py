import tkinter as tk
from tkinter import ttk, messagebox

from src.windows.window import Window
from src.utils.user_settings import UserSettings
from src.utils.get_key_pressed import normalize_key
from src.macro.macro import Macro
from src.hotkeys.hotkeys_manager import HotkeysManager
from src.windows.main.menu_bar import MenuBar


class MainApp(Window):
    def __init__(self):
        super().__init__("MobileGamePCControl", 560, 650)
        self.protocol("WM_DELETE_WINDOW", self.quit_software)
        self.settings = UserSettings(self)
        self.macro = Macro(self)
        self._build_ui()
        self.menu = MenuBar(self)
        self.hotkeyManager = HotkeysManager(self)
        self.update_mode_status_labels()
        self.set_status("Ready")
        self.mainloop()

    def _build_ui(self):
        root = ttk.Frame(self, padding=14)
        root.pack(fill="both", expand=True)

        ttk.Label(root, text="MobileGamePCControl", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(root, text="Configurable keyboard → mouse controls", foreground="#555").pack(anchor="w", pady=(0, 12))

        self.mode1_frame = ttk.LabelFrame(root, text="Mode 1 — Click Trigger", padding=10)
        self.mode1_frame.pack(fill="x", pady=5)
        self._build_mode1(self.mode1_frame)

        self.mode2_frame = ttk.LabelFrame(root, text="Mode 2 — Mouse Hold / ESC", padding=10)
        self.mode2_frame.pack(fill="x", pady=5)
        self._build_mode2(self.mode2_frame)

        info = ttk.LabelFrame(root, text="Key combinations", padding=10)
        info.pack(fill="x", pady=8)
        ttk.Label(info, text="Click Change, then press the desired key or combination.\n"
                           "Example: Shift + ` requires both keys to be held.\n"
                           "Key order does not matter.").pack(anchor="w")

        buttons = ttk.Frame(root)
        buttons.pack(fill="x", pady=(5, 0))
        ttk.Button(buttons, text="Save Settings", command=self.save_settings).pack(side="left")
        ttk.Button(buttons, text="Reset Defaults", command=self.reset_settings).pack(side="left", padx=8)

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(root, textvariable=self.status_var, relief="sunken", anchor="w").pack(fill="x", pady=(12, 0))

    def _build_mode1(self, frame):
        self.mode1_status = ttk.Label(frame)
        self.mode1_status.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))
        self.m1_toggle_var = tk.StringVar()
        self.m1_trigger_var = tk.StringVar()
        self.m1_button_var = tk.StringVar()
        self.m1_behavior_var = tk.StringVar()
        self.m1_interval_var = tk.StringVar()
        self._row_key(frame, 1, "Toggle", "Mode1", "Toggle", self.m1_toggle_var)
        self._row_key(frame, 2, "Trigger", "Mode1", "Trigger", self.m1_trigger_var)
        ttk.Label(frame, text="Mouse button").grid(row=3, column=0, sticky="w", pady=3)
        self.m1_button = ttk.Combobox(frame, textvariable=self.m1_button_var, values=("left", "right", "middle"), state="readonly", width=15)
        self.m1_button.grid(row=3, column=1, sticky="w")
        self.m1_button.bind("<<ComboboxSelected>>", lambda e: self.on_setting_changed())
        ttk.Label(frame, text="Behavior").grid(row=4, column=0, sticky="w", pady=3)
        self.m1_behavior = ttk.Combobox(frame, textvariable=self.m1_behavior_var, values=("rapid", "single"), state="readonly", width=15)
        self.m1_behavior.grid(row=4, column=1, sticky="w")
        self.m1_behavior.bind("<<ComboboxSelected>>", lambda e: self.on_setting_changed())
        ttk.Label(frame, text="Rapid interval (ms)").grid(row=5, column=0, sticky="w", pady=3)
        self.m1_interval = ttk.Spinbox(frame, from_=1, to=10000, textvariable=self.m1_interval_var, width=17, command=self._save_interval)
        self.m1_interval.grid(row=5, column=1, sticky="w")
        self.m1_interval.bind("<FocusOut>", lambda e: self._save_interval())

    def _build_mode2(self, frame):
        self.mode2_status = ttk.Label(frame)
        self.mode2_status.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))
        self.m2_toggle_var = tk.StringVar()
        self.m2_mouse_var = tk.StringVar()
        self.m2_back_var = tk.StringVar()
        self.m2_button_var = tk.StringVar()
        self._row_key(frame, 1, "Toggle", "Mode2", "Toggle", self.m2_toggle_var)
        self._row_key(frame, 2, "Mouse key", "Mode2", "MouseKey", self.m2_mouse_var)
        ttk.Label(frame, text="Mouse button").grid(row=3, column=0, sticky="w", pady=3)
        self.m2_button = ttk.Combobox(frame, textvariable=self.m2_button_var, values=("left", "right", "middle"), state="readonly", width=15)
        self.m2_button.grid(row=3, column=1, sticky="w")
        self.m2_button.bind("<<ComboboxSelected>>", lambda e: self.on_setting_changed())
        self._row_key(frame, 4, "Back / ESC key", "Mode2", "BackKey", self.m2_back_var)

    def _row_key(self, frame, row, label, category, option, variable):
        ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", pady=3)
        ttk.Label(frame, textvariable=variable, width=24).grid(row=row, column=1, sticky="w")
        ttk.Button(frame, text="Change", command=lambda: self.change_key(category, option)).grid(row=row, column=2, sticky="e", padx=(8, 0))

    def format_key_combo(self, combo):
        if isinstance(combo, str):
            combo = [combo]
        names = {"ctrl": "Ctrl", "shift": "Shift", "alt": "Alt", "win": "Win", "altgr": "AltGr", "space": "Space", "esc": "Esc", "enter": "Enter", "tab": "Tab", "backspace": "Backspace", "delete": "Delete", "left": "Left", "right": "Right", "up": "Up", "down": "Down"}
        return " + ".join(names.get(str(k).lower(), str(k)) for k in combo)

    def update_key_label(self, option, combo):
        value = self.format_key_combo(combo)
        mapping = {"Mode1.Toggle": self.m1_toggle_var, "Mode1.Trigger": self.m1_trigger_var,
                   "Mode2.Toggle": self.m2_toggle_var, "Mode2.MouseKey": self.m2_mouse_var, "Mode2.BackKey": self.m2_back_var}
        mapping[f"{option[0]}.{option[1]}"] .set(value)

    def change_key(self, category, option):
        current = self.settings.settings_dict[category].get(option, [])
        dialog = KeyCaptureDialog(self, self.format_key_combo(current))
        self.wait_window(dialog)
        if dialog.result:
            self.settings.change_settings(category, option, newValue=dialog.result)
            self.update_key_label((category, option), dialog.result)
            self.hotkeyManager.reload_config()
            self.set_status(f"Updated {category} {option}")

    def on_setting_changed(self):
        self.settings.settings_dict["Mode1"]["MouseButton"] = self.m1_button_var.get()
        self.settings.settings_dict["Mode1"]["Behavior"] = self.m1_behavior_var.get()
        self.settings.settings_dict["Mode2"]["MouseButton"] = self.m2_button_var.get()
        self.settings.update_settings()
        if hasattr(self, "hotkeyManager"):
            self.hotkeyManager.reload_config()

    def _save_interval(self):
        try:
            value = max(1, int(self.m1_interval_var.get()))
        except ValueError:
            value = 30
        self.m1_interval_var.set(str(value))
        self.settings.change_settings("Mode1", "Interval", newValue=value)
        if hasattr(self, "hotkeyManager"):
            self.hotkeyManager.reload_config()

    def update_mode_status_labels(self):
        if not hasattr(self, "mode1_status"):
            return
        m1 = self.settings.settings_dict["Mode1"]
        m2 = self.settings.settings_dict["Mode2"]
        self.m1_toggle_var.set(self.format_key_combo(m1["Toggle"]))
        self.m1_trigger_var.set(self.format_key_combo(m1["Trigger"]))
        self.m1_button_var.set(m1["MouseButton"])
        self.m1_behavior_var.set(m1["Behavior"])
        self.m1_interval_var.set(str(m1["Interval"]))
        self.m2_toggle_var.set(self.format_key_combo(m2["Toggle"]))
        self.m2_mouse_var.set(self.format_key_combo(m2["MouseKey"]))
        self.m2_button_var.set(m2["MouseButton"])
        self.m2_back_var.set(self.format_key_combo(m2["BackKey"]))
        self.mode1_status.config(text="Status: ON" if m1["Enabled"] else "Status: OFF")
        self.mode2_status.config(text="Status: ON" if m2["Enabled"] else "Status: OFF")

    def save_settings(self):
        self.on_setting_changed()
        self._save_interval()
        self.set_status("Settings saved")

    def reset_settings(self):
        if self.settings.reset_settings():
            self.hotkeyManager.reload_config()
            self.update_mode_status_labels()
            self.set_status("Settings reset to defaults")

    def set_status(self, text):
        self.status_var.set(text)

    def quit_software(self):
        try:
            self.hotkeyManager.stop()
        except Exception:
            pass
        try:
            self.macro.stop_all()
        except Exception:
            pass
        self.destroy()


class KeyCaptureDialog(tk.Toplevel):
    def __init__(self, parent, title, current_keys=None):
        super().__init__(parent)

        self.parent = parent
        self.result = None
        self.pressed_keys = set()
        self.key_order = []

        self.title(title)
        self.geometry("430x220")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.label = tk.Label(
            self,
            text="Press the desired key or key combination",
            font=("Segoe UI", 11),
        )
        self.label.pack(pady=(25, 10))

        self.key_display = tk.Label(
            self,
            text="",
            font=("Segoe UI", 14, "bold"),
        )
        self.key_display.pack(pady=10)

        self.info = tk.Label(
            self,
            text="Hold all desired keys, then release them.",
        )
        self.info.pack(pady=5)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=15)

        tk.Button(
            button_frame,
            text="OK",
            width=10,
            command=self.accept,
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Cancel",
            width=10,
            command=self.cancel,
        ).pack(side="left", padx=5)

        self.bind("<KeyPress>", self.on_key_press)
        self.bind("<KeyRelease>", self.on_key_release)

        self.focus_force()

    # ---------------------------------------------------------
    # Key normalization for Tkinter
    # ---------------------------------------------------------

    @staticmethod
    def get_key_name(event):
        keysym = event.keysym

        # ---------------------------------------------------------
        # Modifier keys
        # ---------------------------------------------------------

        modifiers = {
            "Control_L": "ctrl",
            "Control_R": "ctrl",
            "Shift_L": "shift",
            "Shift_R": "shift",
            "Alt_L": "alt",
            "Alt_R": "alt",
            "Meta_L": "win",
            "Meta_R": "win",
            "Super_L": "win",
            "Super_R": "win",
            "Win_L": "win",
            "Win_R": "win",
        }

        if keysym in modifiers:
            return modifiers[keysym]

        # ---------------------------------------------------------
        # Function keys
        # ---------------------------------------------------------

        if keysym.startswith("F") and keysym[1:].isdigit():
            return keysym.lower()

        # ---------------------------------------------------------
        # Special keys
        # ---------------------------------------------------------

        special = {
            "Escape": "esc",
            "Return": "enter",
            "KP_Enter": "enter",
            "Tab": "tab",
            "BackSpace": "backspace",
            "Delete": "delete",
            "Insert": "insert",
            "Home": "home",
            "End": "end",
            "Prior": "pageup",
            "Next": "pagedown",
            "Up": "up",
            "Down": "down",
            "Left": "left",
            "Right": "right",
            "space": "space",
            "Caps_Lock": "capslock",
            "Num_Lock": "numlock",
            "Scroll_Lock": "scrolllock",
            "Print": "printscreen",
            "Pause": "pause",
        }

        if keysym in special:
            return special[keysym]

        # ---------------------------------------------------------
        # IMPORTANT:
        # Shift + number row must still be recorded as the
        # physical number key.
        #
        # 1 -> !
        # 2 -> @
        # 3 -> #
        # 4 -> $
        # 5 -> %
        # 6 -> ^
        # 7 -> &
        # 8 -> *
        # 9 -> (
        # 0 -> )
        # ---------------------------------------------------------

        shifted_numbers = {
            "exclam": "1",
            "at": "2",
            "numbersign": "3",
            "dollar": "4",
            "percent": "5",
            "asciicircum": "6",
            "ampersand": "7",
            "asterisk": "8",
            "parenleft": "9",
            "parenright": "0",

            # Some Tk/keyboard layouts may report the actual
            # printable symbol instead of the symbolic keysym.
            "!": "1",
            "@": "2",
            "#": "3",
            "$": "4",
            "%": "5",
            "^": "6",
            "&": "7",
            "*": "8",
            "(": "9",
            ")": "0",
        }

        if keysym in shifted_numbers:
            return shifted_numbers[keysym]

        # ---------------------------------------------------------
        # Unshifted number row
        # ---------------------------------------------------------

        if len(keysym) == 1 and keysym.isdigit():
            return keysym

        # ---------------------------------------------------------
        # Normal letters
        # ---------------------------------------------------------

        if len(keysym) == 1 and keysym.isalpha():
            return keysym.lower()

        # ---------------------------------------------------------
        # Punctuation / symbols
        #
        # Both shifted and unshifted forms are converted to the
        # physical key.
        # ---------------------------------------------------------

        punctuation = {
            "grave": "`",
            "asciitilde": "`",

            "minus": "-",
            "underscore": "-",

            "equal": "=",
            "plus": "=",

            "bracketleft": "[",
            "braceleft": "[",

            "bracketright": "]",
            "braceright": "]",

            "backslash": "\\",
            "bar": "\\",

            "semicolon": ";",
            "colon": ";",

            "apostrophe": "'",
            "quotedbl": "'",

            "comma": ",",
            "less": ",",

            "period": ".",
            "greater": ".",

            "slash": "/",
            "question": "/",
        }

        if keysym in punctuation:
            return punctuation[keysym]

        # ---------------------------------------------------------
        # Last resort
        # ---------------------------------------------------------

        char = event.char

        if char and len(char) == 1 and char.isprintable():
            return char.lower()

        return keysym.lower()

    # ---------------------------------------------------------
    # Key events
    # ---------------------------------------------------------

    def on_key_press(self, event):
        key = self.get_key_name(event)

        if not key:
            return

        if key not in self.pressed_keys:
            self.pressed_keys.add(key)
            self.key_order.append(key)

        self.update_display()

    def on_key_release(self, event):
        key = self.get_key_name(event)

        if not key:
            return

        # Don't remove it from key_order.
        #
        # key_order represents the combination the user entered.
        # pressed_keys represents keys currently physically held.
        self.pressed_keys.discard(key)

        self.update_display()

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @staticmethod
    def format_key(key):
        names = {
            "ctrl": "Ctrl",
            "shift": "Shift",
            "alt": "Alt",
            "win": "Win",
            "altgr": "AltGr",
            "esc": "Esc",
            "enter": "Enter",
            "space": "Space",
            "tab": "Tab",
            "backspace": "Backspace",
            "delete": "Delete",
            "insert": "Insert",
            "home": "Home",
            "end": "End",
            "pageup": "Page Up",
            "pagedown": "Page Down",
            "up": "Up",
            "down": "Down",
            "left": "Left",
            "right": "Right",
            "capslock": "Caps Lock",
            "numlock": "Num Lock",
            "scrolllock": "Scroll Lock",
            "printscreen": "Print Screen",
            "pause": "Pause",
        }

        if key in names:
            return names[key]

        if key.startswith("f") and key[1:].isdigit():
            return key.upper()

        return key

    def update_display(self):
        if not self.key_order:
            self.key_display.config(text="")
            return

        display = " + ".join(
            self.format_key(key)
            for key in self.key_order
        )

        self.key_display.config(text=display)

    # ---------------------------------------------------------
    # Dialog buttons
    # ---------------------------------------------------------

    def accept(self):
        if not self.key_order:
            return

        self.result = list(self.key_order)
        self.destroy()

    def cancel(self):
        self.result = None
        self.destroy()
