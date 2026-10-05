import threading
from pynput.mouse import Button, Controller


class Macro:
    def __init__(self, main_app):
        self.main_app = main_app
        self.mouse = Controller()
        self._rapid_thread = None
        self._rapid_stop = threading.Event()
        self._held_buttons = set()
        self._lock = threading.RLock()

    @staticmethod
    def get_mouse_button(name):
        return {
            "left": Button.left,
            "right": Button.right,
            "middle": Button.middle,
        }.get(str(name).lower(), Button.left)

    def click_once(self, button_name="left"):
        with self._lock:
            self.mouse.click(self.get_mouse_button(button_name), 1)

    def start_rapid_click(self, button_name="left", interval=30):
        with self._lock:
            if self._rapid_thread and self._rapid_thread.is_alive():
                return
            try:
                delay = max(float(interval), 1.0) / 1000.0
            except (TypeError, ValueError):
                delay = 0.03
            self._rapid_stop.clear()
            self._rapid_thread = threading.Thread(
                target=self._rapid_click_worker,
                args=(button_name, delay), daemon=True
            )
            self._rapid_thread.start()

    def _rapid_click_worker(self, button_name, delay):
        button = self.get_mouse_button(button_name)
        while not self._rapid_stop.is_set():
            with self._lock:
                self.mouse.click(button, 1)
            self._rapid_stop.wait(delay)

    def stop_rapid_click(self):
        self._rapid_stop.set()
        self._rapid_thread = None

    def mouse_down(self, button_name="left"):
        button = self.get_mouse_button(button_name)
        with self._lock:
            if button not in self._held_buttons:
                self.mouse.press(button)
                self._held_buttons.add(button)

    def mouse_up(self, button_name="left"):
        button = self.get_mouse_button(button_name)
        with self._lock:
            if button in self._held_buttons:
                self.mouse.release(button)
                self._held_buttons.discard(button)

    def release_all_mouse_buttons(self):
        with self._lock:
            for button in list(self._held_buttons):
                try:
                    self.mouse.release(button)
                except Exception:
                    pass
            self._held_buttons.clear()

    def stop_all(self):
        self.stop_rapid_click()
        self.release_all_mouse_buttons()

    def unPressEverything(self):
        self.stop_all()
