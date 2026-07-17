# New Plasma 2350 W: Firmware and Comet Bring-Up

This procedure prepares a new Pimoroni Plasma 2350 W to run this project's
100-LED `comet` pattern. Complete the steps in order and stop at the validation
checks before moving on.

## Result

At the end of this procedure, the board will:

- run the Pimoroni Plasma 2350 W MicroPython firmware;
- have this repository's `device/` files installed;
- start the `comet` pattern automatically after power-up; and
- retain the four-segment layout: `segment_1`, `segment_2`, `segment_3`, and
   `segment_4`, with 25 LEDs in each segment.

## What You Need

- A Pimoroni Plasma 2350 W, connected with a data-capable USB-C cable.
- The LED installation powered safely: strip 5 V to the board's 5 V output,
  strip ground to board ground, and the LED data wire to the Plasma LED data
  connection. All powered parts must share ground.
- A suitable power supply for the installed LED strip. Do not assume USB alone
  can safely power 80 LEDs at full white brightness.
- VS Code with the MicroPico extension configured for this workspace.
- This repository open in VS Code.

## 1. Inspect the Existing Setup

1. Keep the existing physical wiring arrangement unless the new installation
   is intentionally different.
2. Confirm there are 100 WS2812-compatible LEDs in the four physical runs:
   - `segment_1`: indices 0-24
   - `segment_2`: indices 25-49
   - `segment_3`: indices 50-74
   - `segment_4`: indices 75-99
3. Do not power the LEDs from multiple supplies unless their grounds are tied
   together and the power arrangement has been checked first.

The project is configured for `GRB` colour order. A red/green/blue mismatch in
the first animation is normally a colour-order issue, not a failed firmware
flash.

## 2. Download the Correct Firmware

1. Open the official [Plasma releases page](https://github.com/pimoroni/plasma/releases/latest).
2. Select the asset specifically built for **Plasma 2350 W**. Do not use a
   generic RP2350, Pico, Plasma 2350 non-W, or Plasma Stick image.
3. For a newly received board, use the Plasma 2350 W UF2 ending in
   `-with-filesystem.uf2` to start from a known clean filesystem. It includes
   Pimoroni example files and erases existing board files.
4. If preserving files on an already-used board, back them up and use the
   regular Plasma 2350 W UF2 instead. The regular image updates firmware
   without deliberately replacing the filesystem.

At the time this plan was written, the official latest release page reported
Plasma release `v1.1.0`. Always follow the `latest` link above rather than
reusing an old downloaded UF2.

## 3. Flash the Firmware

1. Disconnect **MicroPico vREPL** and close any other serial connection to the
   board.
2. Connect the board by USB-C.
3. Hold the board's **BOOT** button.
4. While still holding BOOT, press and release **RST**.
5. Release BOOT. Windows should show a removable drive named `RP2350`.
6. Copy the downloaded Plasma 2350 W UF2 onto that `RP2350` drive.
7. Wait for the drive to disappear. The board resets itself after a successful
   flash.

Alternative: use MicroPico's firmware-flashing command after selecting the
same Plasma 2350 W UF2. The USB bootloader method above is the upstream
Pimoroni procedure and is the fallback if the extension cannot find the board.

## 4. Verify the Firmware Before Uploading the Project

1. Reconnect to the board with MicroPico vREPL.
2. At the MicroPython prompt, run:

```python
import plasma
import sys
print(sys.implementation)
```

3. The `import plasma` command must complete with no exception. This confirms
   the board-specific Plasma MicroPython firmware is installed.
4. Disconnect vREPL again before uploading files.

If `import plasma` fails, repeat the flash step and verify that the selected
UF2 explicitly names Plasma 2350 W.

## 5. Prepare This Project to Start Comet

The project is configured to start comet in `device/config.py`:

```python
DEFAULT_PATTERN = "comet"
```

This makes the first boot deterministic and makes the visual validation
unambiguous.

Keep these existing settings unless the physical installation differs:

```python
LED_COUNT = 100
COLOR_ORDER = "GRB"
FPS = 60
```

For the first hardware test, leave `BRIGHTNESS_PERCENT` below 100 if the LED
power supply rating is not yet confirmed.

## 6. Upload the Runtime

1. Ensure MicroPico vREPL is disconnected.
2. Make sure MicroPico's sync folder is `device/` for this workspace.
3. Use MicroPico **Upload** to upload the `device/` runtime files. Upload only
   this folder, not the repository root.
4. Reconnect vREPL if needed and issue a soft reset with `Ctrl+D`, or use the
   MicroPico soft-reset command.
5. Disconnect USB power and reconnect it once to check a normal cold boot.

The files that must be present on the board are:

```text
main.py
config.py
segment_mapper.py
patterns/__init__.py
patterns/comet.py
patterns/green_cycle.py
patterns/ten_segment_colors.py
```

`secrets.py` is optional for the visual comet test. It is needed only when the
access point is required; create it from `device/secrets.example.py` and keep
the real credentials out of source control.

## 7. Validate Comet

1. On boot, expect one bright moving head and a five-pixel tail on each of the
   four physical segments.
2. The four heads advance independently around their own segments. Each head
   changes colour when it wraps to the strip start.
3. Check all 100 LEDs light eventually.
4. All four segments are initially configured in forward direction. Set a
   segment's `reversed` value to `True` in `STRIP_DEFS` only if its physical
   direction needs to be reversed.
5. If the colours are wrong but animation works, test `RGB` versus `GRB` in
   `COLOR_ORDER` and re-upload `config.py`.
6. If a whole strip stays dark, power down before checking its data connection,
   orientation, and shared ground.

## 8. Recovery Paths

- **No `RP2350` drive:** use a known data USB-C cable, retry BOOT then RST, and
  avoid USB hubs during first bring-up.
- **`import plasma` fails:** the wrong UF2 was used; reflash the official
  Plasma 2350 W firmware.
- **Upload fails:** disconnect vREPL and all serial tools, confirm the board's
  COM port, then retry MicroPico Upload.
- **Board loops or no pattern:** reconnect vREPL, run `Ctrl+D`, and read the
  traceback. Confirm the complete `device/` folder, including `patterns/`, was
  uploaded.
- **LEDs flicker or reset:** reduce brightness and verify the external LED
  power supply and common ground.

## References

- [Pimoroni Plasma repository](https://github.com/pimoroni/plasma)
- [Latest Plasma firmware release](https://github.com/pimoroni/plasma/releases/latest)
- [Plasma library documentation](https://github.com/pimoroni/plasma/blob/main/docs/plasma.md)
- [Local board reference](board-reference-plasma-2350w.md)
- [Local daily workflow](quick-workflow.md)