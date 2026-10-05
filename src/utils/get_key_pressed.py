_MODIFIER_NORMALIZE = {
    "Key.ctrl_l": "ctrl", "Key.ctrl_r": "ctrl",
    "Key.shift_l": "shift", "Key.shift_r": "shift",
    "Key.alt_l": "alt", "Key.alt_r": "alt",
    "Key.cmd_l": "win", "Key.cmd_r": "win",
    "Key.alt_gr": "altgr",
}


def normalize_key(key):
    if key is None:
        return None
    s = key if isinstance(key, str) else str(key)
    if s in _MODIFIER_NORMALIZE:
        return _MODIFIER_NORMALIZE[s]
    if s.startswith("Key."):
        return s[4:].lower()
    if len(s) >= 2 and s[0] == "'" and s[-1] == "'":
        return s[1:-1]
    return s.lower()


def getKeyPressed(keyboardListener, key):
    try:
        key = keyboardListener.canonical(key)
    except Exception:
        pass
    return normalize_key(key)
