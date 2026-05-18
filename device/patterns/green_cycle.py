def render(ctx, _elapsed, _state, brightness):
    """Move one green pixel from LED 0 to max LED count."""
    ctx["clear_strip"]()

    led_count = max(1, int(ctx["led_count"]))
    position = int(_state.get("green_position", 0)) % led_count
    _state["green_position"] = (position + 1) % led_count

    green = int(255 * max(0.0, min(1.0, brightness)))
    ctx["set_pixel"](position, 0, green, 0)
