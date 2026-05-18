# FlatCapLights

A fun Plasma 2350 W LED project for a hat build.

This repo runs patterns on 80 WS2812 LEDs, split into three fixed physical strips:

- base (0-29)
- top_left (30-54)
- top_right (55-79)

Current default pattern is comet, with one moving head per strip.

## Repo

- device/: board runtime and patterns (this is what you upload)
- docs/: board and workflow notes
- stubs/: local editor stubs so plasma import resolves in VS Code

## Quick start

1. Flash the Plasma 2350 W with Pimoroni Plasma MicroPython firmware.
2. Install the MicroPico extension in VS Code.
3. Open this repo in VS Code.
4. Set MicroPico sync folder to device if needed.
5. Disconnect MicroPico vREPL before upload.
6. Upload the device folder to the board.

## Wi-Fi AP mode

AP startup is enabled in device/config.py

If you are sharing hardware in public, change this password.

## Pattern list

- comet
- green_cycle
- ten_segment_colors
