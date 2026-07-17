import math

from .common import scaled_hsv


def render(ctx, elapsed, _state, brightness):
    """Breathe a color that drifts smoothly around the color wheel."""
    level = 0.12 + 0.88 * ((math.sin(elapsed * 1.7) + 1.0) / 2.0)
    color = scaled_hsv(elapsed * 0.025, 0.85, level, brightness)
    for index in range(int(ctx["led_count"])):
        ctx["set_pixel"](index, *color)