# FlatCapLights

This repo runs patterns on 100 WS2812 LEDs, split into four fixed physical
segments of 25 LEDs:

- segment_1 (0-24)
- segment_2 (25-49)
- segment_3 (50-74)
- segment_4 (75-99)

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

AP startup is enabled in device/config.py.

Create a local credentials file at device/secrets.py (not committed):

```python
AP_SSID = "FlatCap"
AP_PASSWORD = "pie12345"
```

There is a template at device/secrets.example.py.

If you are sharing hardware in public, change the default password.

## Pattern list

- comet
- green_cycle
- ten_segment_colors
