from .common import scaled_hsv


def render(ctx, elapsed, _state, brightness):
    """Bounce a color-shifting scanner with a short fading tail per segment."""
    for strip_number, strip_name in enumerate(ctx["strip_defs"]):
        strip_length = int(ctx["strip_defs"][strip_name]["length"])
        period = max(1, strip_length * 2 - 2)
        step = int(elapsed * 18 + strip_number * 5) % period
        head = step if step < strip_length else period - step
        for local_index in range(strip_length):
            distance = abs(head - local_index)
            level = max(0.0, 1.0 - distance / 6.0)
            color = scaled_hsv(elapsed * 0.05 + strip_number * 0.16, 1.0, level, brightness)
            ctx["set_strip_pixel"](strip_name, local_index, *color)