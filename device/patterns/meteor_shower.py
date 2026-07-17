from .common import scaled_hsv


def render(ctx, elapsed, _state, brightness):
    """Send two color-shifting meteors through every physical segment."""
    for strip_number, strip_name in enumerate(ctx["strip_defs"]):
        strip_length = int(ctx["strip_defs"][strip_name]["length"])
        head_a = int(elapsed * 15 + strip_number * 7) % strip_length
        head_b = int(elapsed * 10 + strip_number * 13 + strip_length // 2) % strip_length
        hue = elapsed * 0.05 + strip_number * 0.18
        for local_index in range(strip_length):
            tail_a = (head_a - local_index) % strip_length
            tail_b = (head_b - local_index) % strip_length
            intensity = 0.0
            if tail_a < 8:
                intensity += (8 - tail_a) / 8.0
            if tail_b < 5:
                intensity += 0.55 * (5 - tail_b) / 5.0
            color = scaled_hsv(hue + local_index * 0.01, 0.8, min(1.0, intensity), brightness)
            ctx["set_strip_pixel"](strip_name, local_index, *color)