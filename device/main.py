import time
import network
import plasma
from pimoroni import Button
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
if config.AP_ENABLED and config.AP_SSID and config.AP_PASSWORD:
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
    "led_enabled": True,
    "last_error": None,
}

sequence_patterns = [
    name for name in getattr(config, "PATTERN_SEQUENCE", ())
    if name in PATTERNS and name != "sequencer"
]
sequence_dwell = max(1, int(getattr(config, "PATTERN_DWELL_SECONDS", 6)))

button_a = None
if getattr(config, "BUTTON_A_ENABLED", True):
    button_a = Button("BUTTON_A", repeat_time=0)
button_a_was_pressed = False
button_a_pressed_at = 0
button_a_long_press_ms = max(1, int(getattr(config, "BUTTON_A_LONG_PRESS_MS", 1000)))


def select_next_pattern():
    if not sequence_patterns:
        return

    current_pattern = runtime_state.get("pattern", config.DEFAULT_PATTERN)
    try:
        current_index = sequence_patterns.index(current_pattern)
    except ValueError:
        current_index = -1
    runtime_state["pattern"] = sequence_patterns[(current_index + 1) % len(sequence_patterns)]

start_ticks = time.ticks_ms()

# Run loop
while True:
    elapsed_ms = time.ticks_diff(time.ticks_ms(), start_ticks)
    elapsed = elapsed_ms / 1000.0

    if button_a:
        button_a_is_pressed = button_a.read()
        if button_a_is_pressed and not button_a_was_pressed:
            button_a_pressed_at = time.ticks_ms()
        elif not button_a_is_pressed and button_a_was_pressed:
            press_duration = time.ticks_diff(time.ticks_ms(), button_a_pressed_at)
            if press_duration >= button_a_long_press_ms:
                runtime_state["led_enabled"] = not runtime_state["led_enabled"]
            else:
                select_next_pattern()
        button_a_was_pressed = button_a_is_pressed

    brightness = clamp(runtime_state["brightness_percent"], 0, 100) / 100.0
    if not runtime_state["led_enabled"]:
        brightness = 0.0

    requested_pattern = runtime_state.get("pattern", config.DEFAULT_PATTERN)
    if requested_pattern == "sequencer" and sequence_patterns:
        sequence_index = int(elapsed // sequence_dwell) % len(sequence_patterns)
        active_pattern = sequence_patterns[sequence_index]
    else:
        active_pattern = requested_pattern

    try:
        render_pattern = resolve_pattern(active_pattern)
        render_pattern(pattern_context, elapsed, runtime_state, brightness)
        runtime_state["last_error"] = None
    except Exception as exc:
        # Keep the board alive and visible even if one pattern fails.
        runtime_state["last_error"] = str(exc)
        runtime_state["pattern"] = "green_cycle"
        clear_strip()

    time.sleep(1.0 / max(1, config.FPS))
