import math


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