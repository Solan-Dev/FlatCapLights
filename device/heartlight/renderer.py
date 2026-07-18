import math
import time


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
    pulse = max(0.0, 1.0 - phase / 0.18)
    level = 0.18 + 0.82 * pulse
    fill(
        ctx,
        int(255 * level * brightness),
        int(54 * level * brightness),
        0,
    )