# MobileGamePCControl

**Version:** 1.0.0
**Platform:** Windows 10 / Windows 11
**Architecture:** Windows x64

MobileGamePCControl (MGPC) is a lightweight Windows utility for configurable keyboard-to-mouse controls.

It is a modified and simplified project derived from **PyMacroRecord** by LOUDO2.

## Features

### Mode 1 — Click Trigger

* Configurable toggle key or key combination
* Configurable trigger key or key combination
* Left, Right, or Middle mouse button
* Single-click behavior
* Rapid-click behavior
* Configurable rapid-click interval
* Persistent settings

Default settings:

* Toggle: `Ctrl + Shift + 1`
* Trigger: `` ` ``
* Mouse button: Left
* Behavior: Rapid
* Interval: 30 ms
* Enabled by default

### Mode 2 — Mouse Hold / ESC

* Configurable toggle key or key combination
* Configurable mouse key or key combination
* Configurable Back / ESC key or key combination
* Left, Right, or Middle mouse button

Default settings:

* Toggle: `Ctrl + Shift + 2`
* Mouse key: `5`
* Mouse button: Left
* Back / ESC key: `6`
* Disabled by default

The Mode 2 mouse key supports both tap and hold behavior:

* Quick press → one mouse click
* Hold → mouse button remains pressed
* Release → mouse button is released

The Back / ESC key sends one Escape key action.

## Key Combinations

The configurable key fields support single keys and combinations.

Examples:

```text
Shift + `
Ctrl + Shift + A
Ctrl + Alt + F8
Win + F12
```

All required keys must be held simultaneously before the configured action starts.

For hold actions, releasing any required key ends the action.

## Configuration

Settings are automatically saved for the current Windows user.

Configuration location:

```text
%LOCALAPPDATA%\MobileGamePCControl\config.json
```

Example:

```text
C:\Users\<YourUserName>\AppData\Local\MobileGamePCControl\config.json
```

The configuration file is created automatically on first launch.

## Running the Application

The release executable is a standalone Windows application.

No Python installation is required to run the released executable.

Run:

```text
MobileGamePCControl.exe
```

## Resetting Settings

Settings can be restored to their defaults using:

**Settings → Reset to Defaults**

or the **Reset Defaults** button.

## Building From Source

Python 3.13 or a compatible Python version is recommended.

Create and activate a virtual environment, then install the required dependencies.

Example:

```powershell
cd D:\CMD\MobileGamePCControl
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

To build the Windows standalone executable with PyInstaller:

```powershell
python -m PyInstaller --clean --noconfirm --onefile --windowed --name MobileGamePCControl main.py
```

The resulting executable will be placed in:

```text
dist\MobileGamePCControl.exe
```

## Project Origin and Attribution

MobileGamePCControl is a modified and simplified derivative of:

**PyMacroRecord**

Original project:

https://github.com/LOUDO2/PyMacroRecord

Original project author:

**LOUDO2**

PyMacroRecord is released under the **GNU General Public License v3.0 (GPL-3.0)**.

MobileGamePCControl retains the applicable GPL-3.0 licensing requirements for code derived from PyMacroRecord.

The original PyMacroRecord project and its authors remain credited for the original work.

## Changes From PyMacroRecord

MobileGamePCControl is not intended to be a full macro recorder.

The project was substantially simplified and adapted to focus on configurable keyboard-to-mouse control.

Features from the original application that are not part of MGPC include, among others:

* Macro recording
* Macro playback
* Macro file management
* Recording mouse movement
* Recording keyboard input
* Recording mouse clicks
* Playback scheduling
* Playback repeat management
* Playback speed controls
* Other full macro-recorder functionality

MGPC instead focuses on its two configurable control modes.

## License

MobileGamePCControl is distributed under the **GNU General Public License v3.0 (GPL-3.0)**, in accordance with the licensing requirements applicable to the GPL-licensed source from which this project was derived.

See the `LICENSE.md` file included with this repository for the complete license text.

## Disclaimer

This software is provided without warranty.

The author and contributors are not responsible for damage, data loss, unintended input, software conflicts, or other consequences resulting from use of this software.

Users are responsible for complying with the rules, terms of service, and policies of any software, game, website, or service with which they use MobileGamePCControl.

## Release

### v1.0.0

Initial MobileGamePCControl release.

* Configurable Mode 1
* Configurable Mode 2
* Single and rapid clicking
* Mouse button selection
* Keyboard combinations
* Persistent configuration
* Windows standalone executable
* Reset-to-default settings
* GPL-3.0 licensing and PyMacroRecord attribution
