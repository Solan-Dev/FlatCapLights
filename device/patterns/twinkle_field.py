from .common import scaled_hsv


def render(ctx, elapsed, _state, brightness):
    """Create a field of deterministic, gently fading colored twinkles."""
    tick = int(elapsed * 11)
    for index in range(int(ctx["led_count"])):
        seed = (index * 73 + tick * 151 + index * tick * 3) % 101
        if seed < 12:
            level = (12 - seed) / 12.0
            color = scaled_hsv(elapsed * 0.06 + index * 0.047, 0.55, level, brightness)
        else:
            color = (0, 0, 0)
        ctx["set_pixel"](index, *color)