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
- LEDs: 70 total, arranged as four segments of 17, 18, 18, and 17 LEDs
- Default pattern: comet
- Frame rate: 60 FPS

## Daily Loop

1. Make sure `MicroPico vREPL` is disconnected before uploading.
2. Edit files in `device/`.
3. Upload the complete runtime from the repository root:

	```powershell
	python scripts/upload_device.py
	```

	The uploader uses `COM5` by default. If Windows assigns another port, run:

	```powershell
	python scripts/upload_device.py --port COM7
	```

4. The uploader removes stale matching `.mpy` files, uploads the source, then
	soft-resets the board so the updated pattern starts automatically.
5. Reconnect vREPL only when you want to inspect the board.

## What Goes Where

- Put board constants in `device/config.py`.
- Put hardware setup and the main loop in `device/main.py`.
- Put each pattern in its own file under `device/patterns/`.
- Register pattern names in `device/patterns/__init__.py`.
- Keep board-facing code small and easy to upload.
- `scripts/upload_device.py` uploads every runtime `.py` file in `device/` and
	excludes `secrets.example.py`. A real `device/secrets.py`, when present, is
	uploaded.

## Button A

- A short Button A press selects the next pattern in `PATTERN_SEQUENCE`.
- Hold Button A for one second to toggle the LEDs on or off.
- Change the pattern order or hold duration in `device/config.py`.
- Do not use the BOOT button for normal controls; it is needed for firmware
	flashing.

## If Upload Fails

- Check whether MicroPico vREPL or another serial tool still has the COM port
	open.
- Confirm the board is visible on the expected COM port.
- Run `python scripts/upload_device.py --port COMx` with the detected port.
- Verify the Plasma firmware is installed, not a generic MicroPython build.

## Current Teaching Goal

We are rebuilding the project from simple pieces:

1. One file for board setup
2. One file for constants
3. One effect at a time
4. Optional control features later
