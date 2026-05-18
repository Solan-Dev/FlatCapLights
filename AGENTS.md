# HatLights Agent Notes

This repository is a teaching workspace for the Plasma 2350 W board.

## Work Style

- Keep the live board code in `device/`.
- Treat `docs/` as the source of truth for setup and workflow notes.
- Prefer small, explainable changes.
- Do not reintroduce terminal deploy scripts unless the user asks for them.
- Use MicroPico for upload and vREPL access.
- Disconnect `MicroPico vREPL` before any upload.

## Current Board Facts

- Board: Plasma 2350 W
- Firmware: Pimoroni Plasma MicroPython image with `import plasma`
- LEDs: 80 total
- Physical layout model: `STRIP_DEFS` (`start`, `length`, `reversed`) is canonical
- Strip names: `base`, `top_left`, `top_right`
- Default pattern: `comet`
- AP mode: enabled (`FlatCap`)
- Frame rate: 60 FPS

## Important Files

- `device/main.py` - board startup and loop
- `device/config.py` - constants, AP config, and canonical strip definitions
- `device/segment_mapper.py` - strip and optional segment mapping helpers
- `device/patterns/` - one pattern per file plus registry
- `docs/quick-workflow.md` - daily development loop
- `docs/board-reference-plasma-2350w.md` - hardware and firmware notes
- `docs/http-api-reference.md` - runtime control API

## Development Rules

- Keep settings in `device/config.py`.
- Keep upload targets limited to `device/`.
- Prefer `plasma.WS2812` and `strip.start(config.FPS)` for this board.
- Prefer strip-local addressing in patterns through `segment_mapper` and runtime helpers.
- Add new patterns as new files in `device/patterns/` and register them by name.
- When adding behavior, start with the simplest working loop, then layer complexity.
