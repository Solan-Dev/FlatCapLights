import time

from patterns.common import scaled_hsv


UNICORN_CYCLE_SECONDS = 20
UNICORN_DURATION_SECONDS = 4


def render_searching(ctx, elapsed, brightness):
    """Render a strong synthetic red heartbeat while the watch is unavailable."""
    phase = elapsed % 1.0
    primary = max(0.0, 1.0 - abs(phase - 0.12) / 0.12)
    secondary = max(0.0, 1.0 - abs(phase - 0.34) / 0.08)
    pulse = max(primary, secondary * 0.55)
    level = 0.14 + 0.86 * pulse
    red = int(255 * level * brightness)
    green = int(18 * level * brightness)

    for index in range(int(ctx["led_count"])):
        ctx["set_pixel"](index, red, green, 0)


def fill(ctx, red, green, blue):
    for index in range(int(ctx["led_count"])):
        ctx["set_pixel"](index, red, green, blue)


def render_segment_rainbow(ctx, elapsed, level, brightness):
    for strip_number, strip_name in enumerate(ctx["strip_defs"]):
        hue = elapsed * 0.045 + strip_number / 4.0
        color = scaled_hsv(hue, 0.9, level, brightness)
        strip_length = int(ctx["strip_defs"][strip_name]["length"])
        for local_index in range(strip_length):
            ctx["set_strip_pixel"](strip_name, local_index, *color)


def render_unicorn(ctx, elapsed, level, brightness):
    visual_index = 0
    led_count = max(1, int(ctx["led_count"]))
    for strip_name in ctx["strip_defs"]:
        strip_length = int(ctx["strip_defs"][strip_name]["length"])
        for local_index in range(strip_length):
            hue = elapsed * 0.09 + visual_index / led_count
            color = scaled_hsv(hue, 0.95, level, brightness)
            ctx["set_strip_pixel"](strip_name, local_index, *color)
            visual_index += 1


def render(ctx, elapsed, state, brightness):
    """Render searching, confirmation, and live heart-rate LED states."""
    now_ms = time.ticks_ms()
    if not state.connected or state.last_update_ms is None:
        render_searching(ctx, elapsed, brightness)
        return

    if time.ticks_diff(now_ms, state.connected_at_ms) < 700:
        fill(ctx, 0, int(255 * brightness), 0)
        return

    if time.ticks_diff(now_ms, state.last_update_ms) >= 3000:
        render_searching(ctx, elapsed, brightness)
        return

    period_ms = max(1, state.beat_period_ms)
    beat_age = time.ticks_diff(now_ms, state.beat_anchor_ms) % period_ms
    phase = beat_age / period_ms
    primary_pulse = max(0.0, 1.0 - phase / 0.16)
    secondary_pulse = 0.38 * max(0.0, 1.0 - abs(phase - 0.34) / 0.09)
    pulse = max(primary_pulse, secondary_pulse)
    level = 0.18 + 0.82 * pulse
    if elapsed % UNICORN_CYCLE_SECONDS < UNICORN_DURATION_SECONDS:
        render_unicorn(ctx, elapsed, level, brightness)
    else:
        render_segment_rainbow(ctx, elapsed, level, brightness)