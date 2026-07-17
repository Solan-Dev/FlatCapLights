import math

from .common import scaled_hsv


def render(ctx, elapsed, _state, brightness):
    """Drift layered green, cyan, and violet aurora ribbons across the LEDs."""
    led_count = max(1, int(ctx["led_count"]))
    for index in range(led_count):
        position = index / led_count
        wave = (math.sin(position * 13.0 - elapsed * 1.1) + 1.0) / 2.0
        shimmer = (math.sin(position * 29.0 + elapsed * 0.8) + 1.0) / 2.0
        hue = 0.34 + 0.28 * shimmer
        color = scaled_hsv(hue, 0.75, 0.12 + 0.88 * wave, brightness)
        ctx["set_pixel"](index, *color)