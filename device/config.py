# Total number of physical LEDs on the strips.
LED_COUNT = 80
# Byte order expected by the LED strips (common values: RGB, GRB).
COLOR_ORDER = "GRB"
# Refresh rate used by the plasma driver.
FPS = 60
# Pattern to run at startup if no runtime override exists.
DEFAULT_PATTERN = "comet"
# Global pattern brightness percentage.
BRIGHTNESS_PERCENT = 100

# Access Point settings.
AP_ENABLED = True
AP_SSID = ""
AP_PASSWORD = ""

# Physical strip layout in 3D space.
# These ranges are fixed wiring truth and should rarely change.
STRIP_DEFS = {
	"base": {"start": 0, "length": 30, "reversed": False},
	"top_left": {"start": 30, "length": 25, "reversed": True},
	"top_right": {"start": 55, "length": 25, "reversed": False},
}

