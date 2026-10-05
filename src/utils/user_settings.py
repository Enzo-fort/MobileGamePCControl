import json
import os
from pathlib import Path
from tkinter import messagebox


class UserSettings:
    DEFAULT_SETTINGS = {
        "Mode1": {
            "Enabled": True,
            "Toggle": ["ctrl", "shift", "1"],
            "Trigger": ["`"],
            "MouseButton": "left",
            "Behavior": "rapid",
            "Interval": 30,
        },
        "Mode2": {
            "Enabled": False,
            "Toggle": ["ctrl", "shift", "2"],
            "MouseKey": ["5"],
            "MouseButton": "left",
            "BackKey": ["6"],
        },
    }

    def __init__(self, main_app):
        self.main_app = main_app
        base = os.getenv("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
        self.path_setting = Path(base) / "MobileGamePCControl"
        self.user_setting = self.path_setting / "config.json"
        self.path_setting.mkdir(parents=True, exist_ok=True)
        if self.user_setting.exists():
            self.settings_dict = self._load_settings()
        else:
            self.settings_dict = self._default_settings()
            self.update_settings()
        self.check_new_options()

    def _default_settings(self):
        return json.loads(json.dumps(self.DEFAULT_SETTINGS))

    def _load_settings(self):
        try:
            with self.user_setting.open("r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, dict) else self._default_settings()
        except (OSError, json.JSONDecodeError):
            return self._default_settings()

    def update_settings(self):
        self.path_setting.mkdir(parents=True, exist_ok=True)
        tmp = self.user_setting.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(self.settings_dict, f, indent=4)
        tmp.replace(self.user_setting)

    def get_path(self):
        return str(self.path_setting)

    def change_settings(self, category, option=None, option2=None, newValue=None):
        if category not in self.settings_dict:
            self.settings_dict[category] = {}
        if option is None:
            self.settings_dict[category] = newValue
        elif option2 is not None:
            self.settings_dict[category][option][option2] = newValue
        else:
            self.settings_dict[category][option] = newValue
        self.update_settings()

    def reset_settings(self):
        if messagebox.askyesno("Reset settings", "Reset all MobileGamePCControl settings to defaults?"):
            self.settings_dict = self._default_settings()
            self.update_settings()
            return True
        return False

    def check_new_options(self):
        changed = False
        defaults = self._default_settings()
        for category, values in defaults.items():
            if category not in self.settings_dict:
                self.settings_dict[category] = values
                changed = True
                continue
            for option, value in values.items():
                if option not in self.settings_dict[category]:
                    self.settings_dict[category][option] = value
                    changed = True

        for category, options in (("Mode1", ("Toggle", "Trigger")), ("Mode2", ("Toggle", "MouseKey", "BackKey"))):
            for option in options:
                value = self.settings_dict[category].get(option)
                if isinstance(value, str):
                    self.settings_dict[category][option] = [value]
                    changed = True
                elif not isinstance(value, list) or not value:
                    self.settings_dict[category][option] = defaults[category][option]
                    changed = True

        for category in ("Mode1", "Mode2"):
            if self.settings_dict[category].get("MouseButton") not in ("left", "right", "middle"):
                self.settings_dict[category]["MouseButton"] = "left"
                changed = True

        if self.settings_dict["Mode1"].get("Behavior") not in ("rapid", "single"):
            self.settings_dict["Mode1"]["Behavior"] = "rapid"
            changed = True
        try:
            interval = int(self.settings_dict["Mode1"].get("Interval", 30))
            if interval < 1:
                raise ValueError
            self.settings_dict["Mode1"]["Interval"] = interval
        except (TypeError, ValueError):
            self.settings_dict["Mode1"]["Interval"] = 30
            changed = True
        if changed:
            self.update_settings()
