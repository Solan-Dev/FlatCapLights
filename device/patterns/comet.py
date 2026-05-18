def render(ctx, _elapsed, state, brightness):
    """One comet per strip with a 5-pixel tail at 80% head brightness."""
    scale = max(0.0, min(1.0, brightness))

    # Simple high-contrast palette for loop-to-loop color changes.
    palette = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 0),
        (255, 0, 255),
        (0, 255, 255),
    ]

    strip_defs = ctx["strip_defs"]
    positions = state.setdefault("comet_positions", {})
    color_indexes = state.setdefault("comet_color_indexes", {})

    for strip_name in strip_defs:
        strip_len = int(strip_defs[strip_name]["length"])
        if strip_len <= 0:
            continue

        position = int(positions.get(strip_name, 0)) % strip_len
        color_index = int(color_indexes.get(strip_name, 0)) % len(palette)
        head_r, head_g, head_b = palette[color_index]

        # Paint the full strip in one pass to avoid clear/repaint flicker.
        for local_index in range(strip_len):
            distance = (position - local_index) % strip_len

            if distance == 0:
                multiplier = 1.0
            elif 1 <= distance <= 5:
                multiplier = 0.8
            else:
                multiplier = 0.0

            ctx["set_strip_pixel"](
                strip_name,
                local_index,
                int(head_r * scale * multiplier),
                int(head_g * scale * multiplier),
                int(head_b * scale * multiplier),
            )

        next_position = (position + 1) % strip_len
        positions[strip_name] = next_position

        if next_position == 0:
            color_indexes[strip_name] = (color_index + 1) % len(palette)
        else:
            color_indexes[strip_name] = color_index
