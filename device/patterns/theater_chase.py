from .common import scaled_hsv


def render(ctx, elapsed, _state, brightness):
    """Run spaced theater-chase lights through each physical segment."""
    phase = int(elapsed * 8) % 3
    hue = elapsed * 0.07
    for strip_number, strip_name in enumerate(ctx["strip_defs"]):
        strip_length = int(ctx["strip_defs"][strip_name]["length"])
        color = scaled_hsv(hue + strip_number * 0.12, 1.0, 1.0, brightness)
        for local_index in range(strip_length):
            if (local_index + phase) % 3 == 0:
                ctx["set_strip_pixel"](strip_name, local_index, *color)
            else:
                ctx["set_strip_pixel"](strip_name, local_index, 0, 0, 0)