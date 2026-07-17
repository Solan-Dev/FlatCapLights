from .common import scaled_hsv


def render(ctx, elapsed, _state, brightness):
    """Move a continuously shifting rainbow along the full installation."""
    led_count = max(1, int(ctx["led_count"]))
    for index in range(led_count):
        color = scaled_hsv(elapsed * 0.08 + index / led_count, 1.0, 1.0, brightness)
        ctx["set_pixel"](index, *color)