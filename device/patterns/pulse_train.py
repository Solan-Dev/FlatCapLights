from .common import scaled_hsv


def render(ctx, elapsed, _state, brightness):
    """Send several colored light packets through the complete installation."""
    led_count = max(1, int(ctx["led_count"]))
    head = int(elapsed * 20) % led_count
    for index in range(led_count):
        distance = (head - index) % led_count
        pulse_offset = distance % 28
        level = 0.0
        if pulse_offset < 8:
            level = (8 - pulse_offset) / 8.0
        color = scaled_hsv(elapsed * 0.08 + distance * 0.008, 0.95, level, brightness)
        ctx["set_pixel"](index, *color)