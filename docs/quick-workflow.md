# Quick Workflow

This project is set up to be edited and uploaded in `device/` only.

## Layout

- `device/` - MicroPython files that go onto the board.
- `docs/` - working notes and board references.
- `.vscode/` - editor settings for MicroPico and Python.
- `.micropico` - project marker used by MicroPico.

## Current Board Assumptions

- Board: Plasma 2350 W
- Firmware: Pimoroni Plasma MicroPython build with `import plasma`
- LEDs: 100 total
- Default pattern: one green LED cycles from 0 to 99
- Frame rate: 60 FPS

## Daily Loop

1. Make sure `MicroPico vREPL` is disconnected before uploading.
2. Edit `device/main.py` or `device/config.py`.
3. Use MicroPico to upload the `device/` folder or the changed file.
4. Reconnect vREPL only when you want to test or inspect the board.
5. Press `Ctrl+D` in vREPL for a soft reset after changes.

## What Goes Where

- Put board constants in `device/config.py`.
- Put hardware setup and the main loop in `device/main.py`.
- Put each pattern in its own file under `device/patterns/`.
- Register pattern names in `device/patterns/__init__.py`.
- Keep board-facing code small and easy to upload.

## If Upload Fails

- Check whether `MicroPico vREPL` is still open.
- Confirm the board is visible on the expected COM port.
- Verify the Plasma firmware is installed, not a generic MicroPython build.
- If needed, reconnect the board and try again after closing all serial sessions.

## Current Teaching Goal

We are rebuilding the project from simple pieces:

1. One file for board setup
2. One file for constants
3. One effect at a time
4. Optional control features later
