from .common import scaled_hsv


def render(ctx, elapsed, _state, brightness):
    """Scatter brief, color-changing confetti flashes against black."""
    tick = int(elapsed * 18)
    for index in range(int(ctx["led_count"])):
        seed = (index * 97 + tick * 41 + index * tick * 5) % 127
        if seed < 9:
            level = (9 - seed) / 9.0
            color = scaled_hsv(elapsed * 0.09 + index * 0.071, 0.9, level, brightness)
        else:
            color = (0, 0, 0)
        ctx["set_pixel"](index, *color)