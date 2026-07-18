import asyncio
import time
import network
import plasma
from pimoroni import Button
import config
from heartlight.ble_manager import HeartRateBleManager
from heartlight.cadence_renderer import render as render_cadence
from heartlight.renderer import render as render_heart_rate
from heartlight.state import HeartRateState
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
    "mode": config.DEFAULT_PATTERN,
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
heart_rate_mode = getattr(config, "HEART_RATE_MODE", "heart_rate")
cadence_mode = getattr(config, "CADENCE_MODE", "cadence")
ble_modes = (heart_rate_mode, cadence_mode)
mode_sequence = [
    name for name in getattr(config, "MODE_SEQUENCE", sequence_patterns)
    if name in PATTERNS or name in ble_modes
]

button_a = None
if getattr(config, "BUTTON_A_ENABLED", True):
    button_a = Button("BUTTON_A", repeat_time=0)
button_a_was_pressed = False
button_a_pressed_at = 0
button_a_long_press_ms = max(1, int(getattr(config, "BUTTON_A_LONG_PRESS_MS", 1000)))


def select_next_mode():
    if not mode_sequence:
        return

    current_mode = runtime_state.get("mode", config.DEFAULT_PATTERN)
    try:
        current_index = mode_sequence.index(current_mode)
    except ValueError:
        current_index = -1
    next_mode = mode_sequence[(current_index + 1) % len(mode_sequence)]
    runtime_state["mode"] = next_mode
    if next_mode in PATTERNS:
        runtime_state["pattern"] = next_mode

heart_state = HeartRateState(
    period_window=getattr(config, "HEART_RATE_PERIOD_WINDOW", 5),
)
ble_manager = HeartRateBleManager(
    heart_state,
    diagnostics=getattr(config, "BLE_DIAGNOSTICS", False),
)
active_mode = None
ble_task = None


async def set_active_mode(next_mode):
    global active_mode, ble_task
    if next_mode == active_mode:
        return

    if ble_task and next_mode not in ble_modes:
        ble_manager.stop()
        ble_task.cancel()
        try:
            await ble_task
        except asyncio.CancelledError:
            pass
        ble_task = None
        heart_state.reset_connection()

    if ap:
        ap.active(next_mode not in ble_modes)

    if next_mode in ble_modes and not ble_task:
        ble_task = asyncio.create_task(ble_manager.discovery_loop())

    active_mode = next_mode


async def run():
    global button_a_was_pressed, button_a_pressed_at
    start_ticks = time.ticks_ms()

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
                    select_next_mode()
            button_a_was_pressed = button_a_is_pressed

        selected_mode = runtime_state.get("mode", config.DEFAULT_PATTERN)
        await set_active_mode(selected_mode)

        brightness = clamp(runtime_state["brightness_percent"], 0, 100) / 100.0
        if not runtime_state["led_enabled"]:
            brightness = 0.0

        try:
            if selected_mode == heart_rate_mode:
                render_heart_rate(pattern_context, elapsed, heart_state, brightness)
            elif selected_mode == cadence_mode:
                render_cadence(pattern_context, elapsed, heart_state, brightness)
            else:
                requested_pattern = runtime_state.get("pattern", config.DEFAULT_PATTERN)
                if requested_pattern == "sequencer" and sequence_patterns:
                    sequence_index = int(elapsed // sequence_dwell) % len(sequence_patterns)
                    active_pattern = sequence_patterns[sequence_index]
                else:
                    active_pattern = requested_pattern
                resolve_pattern(active_pattern)(pattern_context, elapsed, runtime_state, brightness)
            runtime_state["last_error"] = None
        except Exception as exc:
            runtime_state["last_error"] = str(exc)
            clear_strip()

        await asyncio.sleep_ms(max(1, int(1000 / max(1, config.FPS))))


asyncio.run(run())
