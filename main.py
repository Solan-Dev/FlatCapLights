# Root bootstrap for MicroPython boards.
# This ensures startup works whether project files are synced to root
# or under a device/ package folder.
try:
    import device.main  # noqa: F401
except ImportError as exc:
    import time

    try:
        print("Startup import failed:", exc)
    except Exception:
        pass

    # Keep board alive for serial diagnostics if import fails.
    while True:
        time.sleep(1)
