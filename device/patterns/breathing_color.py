import math

from .common import scaled_hsv


def render(ctx, elapsed, _state, brightness):
    """Breathe each physical segment independently with a drifting color."""
    for strip_number, strip_name in enumerate(ctx["strip_defs"]):
        phase = elapsed * 1.2 + strip_number * 1.57
        level = 0.12 + 0.88 * ((math.sin(phase) + 1.0) / 2.0)
        color = scaled_hsv(elapsed * 0.025 + strip_number * 0.17, 0.85, level, brightness)
        strip_length = int(ctx["strip_defs"][strip_name]["length"])
        for local_index in range(strip_length):
            ctx["set_strip_pixel"](strip_name, local_index, *color)