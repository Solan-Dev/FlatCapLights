import time
import network
import plasma
import config
from patterns import PATTERNS
from segment_mapper import validate_strip_defs, strip_local_to_global

# Initialize the physical LED strip with configured LED count and color order.
color_order_name = "COLOR_ORDER_{}".format(config.COLOR_ORDER.upper())
color_order = getattr(plasma, color_order_name, plasma.COLOR_ORDER_RGB)
strip = plasma.WS2812(config.LED_COUNT, color_order=color_order)
# Start the strip refresh loop at the configured frame rate.
strip.start(config.FPS)

ap = None
if config.AP_ENABLED:
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=config.AP_SSID, password=config.AP_PASSWORD)

# Validate fixed physical strip layout at startup.
validate_strip_defs(config.STRIP_DEFS, config.LED_COUNT)


# Set one physical LED to an RGB color.
def set_pixel(index, red, green, blue):
    strip.set_rgb(index, red, green, blue)


# Turn all LEDs off.
def clear_strip():
    for index in range(config.LED_COUNT):
        set_pixel(index, 0, 0, 0)


# Set one pixel using strip-local addressing.
def set_strip_pixel(strip_name, local_index, red, green, blue):
    global_index = strip_local_to_global(config.STRIP_DEFS, strip_name, local_index)
    set_pixel(global_index, red, green, blue)


# Fill a full physical strip with one color.
def fill_strip(strip_name, red, green, blue):
    strip_len = int(config.STRIP_DEFS[strip_name]["length"])
    for local_index in range(strip_len):
        set_strip_pixel(strip_name, local_index, red, green, blue)


# Clamp a value between low and high.
def clamp(value, low, high):
    if value < low:
        return low
    if value > high:
        return high
    return value

# Resolve requested pattern name and fall back to default if missing.
def resolve_pattern(pattern_name):
    return PATTERNS.get(pattern_name, PATTERNS[config.DEFAULT_PATTERN])

pattern_context = {
    "led_count": config.LED_COUNT,
    "clear_strip": clear_strip,
    "set_pixel": set_pixel,
    "strip_defs": config.STRIP_DEFS,
    "set_strip_pixel": set_strip_pixel,
    "fill_strip": fill_strip,
}

runtime_state = {
    "pattern": config.DEFAULT_PATTERN,
    "brightness_percent": config.BRIGHTNESS_PERCENT,
}

start_ticks = time.ticks_ms()

# Run loop
while True:
    elapsed_ms = time.ticks_diff(time.ticks_ms(), start_ticks)
    elapsed = elapsed_ms / 1000.0

    brightness = clamp(runtime_state["brightness_percent"], 0, 100) / 100.0
    render_pattern = resolve_pattern(runtime_state["pattern"])
    render_pattern(pattern_context, elapsed, runtime_state, brightness)

    time.sleep(1.0 / max(1, config.FPS))
