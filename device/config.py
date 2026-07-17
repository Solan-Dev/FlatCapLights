# Total number of physical LEDs on the strips.
LED_COUNT = 100
# Byte order expected by the LED strips (common values: RGB, GRB).
COLOR_ORDER = "GRB"
# Refresh rate used by the plasma driver.
FPS = 60
# Pattern to run at startup if no runtime override exists.
DEFAULT_PATTERN = "comet"
# Global pattern brightness percentage.
BRIGHTNESS_PERCENT = 100

# Pattern order for Button A and optional sequencer mode.
PATTERN_SEQUENCE = (
	"comet",
	"rainbow_sweep",
	"breathing_color",
	"meteor_shower",
	"twinkle_field",
	"color_wipe",
	"theater_chase",
	"larson_scanner",
	"aurora",
	"pulse_train",
	"confetti",
)
PATTERN_DWELL_SECONDS = 6

# Button A controls.
# A short press selects the next pattern; holding it toggles LEDs on or off.
BUTTON_A_ENABLED = True
BUTTON_A_LONG_PRESS_MS = 1000

# Access Point settings.
AP_ENABLED = True
try:
	import secrets as _secrets
except ImportError:
	_secrets = None

AP_SSID = getattr(_secrets, "AP_SSID", None)
AP_PASSWORD = getattr(_secrets, "AP_PASSWORD", None)

# Physical strip layout in 3D space.
# These ranges are fixed wiring truth and should rarely change.
STRIP_DEFS = {
	"segment_1": {"start": 0, "length": 25, "reversed": True},
	"segment_2": {"start": 25, "length": 25, "reversed": True},
	"segment_3": {"start": 50, "length": 25, "reversed": True},
	"segment_4": {"start": 75, "length": 25, "reversed": True},
}

