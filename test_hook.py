import time

from src.hotkeys.windows_hook import WindowsKeyboardHook


def callback(vk, down, up, flags):
    print(
        f"VK={vk} "
        f"DOWN={down} "
        f"UP={up} "
        f"FLAGS={flags}",
        flush=True,
    )

    # Suppress grave key (VK_OEM_3 = 0xC0)
    if vk == 0xC0:
        return True

    return False


hook = WindowsKeyboardHook(callback)

print("Starting hook...", flush=True)

if not hook.start():
    print(
        f"HOOK FAILED: {hook.last_error}",
        flush=True,
    )
    raise SystemExit(1)

print("HOOK INSTALLED.", flush=True)
print("Press the ` key. Press Ctrl+C to exit.", flush=True)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping...", flush=True)
finally:
    hook.stop()
