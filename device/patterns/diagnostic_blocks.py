def render(ctx, _elapsed, _state, brightness):
    """Show consecutive 10-LED blocks in distinct repeating diagnostic colors."""
    scale = max(0.0, min(1.0, brightness))
    colors = (
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
    )

    for index in range(int(ctx["led_count"])):
        red, green, blue = colors[(index // 10) % len(colors)]
        ctx["set_pixel"](
            index,
            int(red * scale),
            int(green * scale),
            int(blue * scale),
        )