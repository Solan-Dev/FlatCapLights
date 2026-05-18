def render(ctx, _elapsed, _state, brightness):
    """Quick test pattern: 10 segments x 10 LEDs, each with a different color."""
    scale = max(0.0, min(1.0, brightness))
    colors = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 0),
        (255, 0, 255),
        (0, 255, 255),
        (255, 128, 0),
        (128, 0, 255),
        (255, 255, 255),
        (64, 128, 255),
    ]

    led_count = int(ctx["led_count"])
    for i in range(led_count):
        segment_index = min(9, i // 10)
        r, g, b = colors[segment_index]
        ctx["set_pixel"](i, int(r * scale), int(g * scale), int(b * scale))
