from .common import scaled_hsv


def render(ctx, elapsed, _state, brightness):
    """Wipe a continuously changing color across the full LED installation."""
    led_count = max(1, int(ctx["led_count"]))
    phase = int(elapsed * 24) % (led_count + 12)
    color = scaled_hsv(elapsed * 0.06, 0.9, 1.0, brightness)
    for index in range(led_count):
        if index < phase:
            ctx["set_pixel"](index, *color)
        else:
            ctx["set_pixel"](index, 0, 0, 0)