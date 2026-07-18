import time


LEFT_STRIPS = ("segment_1", "segment_2")
RIGHT_STRIPS = ("segment_3", "segment_4")


def fill_strip(ctx, strip_name, color):
    strip_length = int(ctx["strip_defs"][strip_name]["length"])
    for local_index in range(strip_length):
        ctx["set_strip_pixel"](strip_name, local_index, *color)


def render_searching(ctx, elapsed, brightness):
    phase = elapsed % 1.0
    level = 0.08 + 0.45 * max(0.0, 1.0 - phase / 0.22)
    color = (int(255 * level * brightness), int(40 * level * brightness), 0)
    for strip_name in ctx["strip_defs"]:
        fill_strip(ctx, strip_name, color)


def render(ctx, elapsed, state, brightness):
    """Render inferred alternating steps from real aggregate running cadence."""
    now_ms = time.ticks_ms()
    if (
        not state.connected
        or state.cadence_spm is None
        or state.last_cadence_update_ms is None
        or time.ticks_diff(now_ms, state.last_cadence_update_ms) >= 3000
    ):
        render_searching(ctx, elapsed, brightness)
        return

    step_period_ms = max(1, int(60000 / max(1, state.cadence_spm)))
    step_age_ms = time.ticks_diff(now_ms, state.step_anchor_ms) % step_period_ms
    phase = step_age_ms / step_period_ms
    landing = max(0.0, 1.0 - phase / 0.22)
    landing *= landing
    step_index = time.ticks_diff(now_ms, state.step_anchor_ms) // step_period_ms
    active_strips = LEFT_STRIPS if step_index % 2 == 0 else RIGHT_STRIPS

    active_color = (
        int(25 * landing * brightness),
        int(255 * landing * brightness),
        int(215 * landing * brightness),
    )
    resting_color = (
        int(5 * brightness),
        int(16 * brightness),
        int(18 * brightness),
    )
    for strip_name in ctx["strip_defs"]:
        color = active_color if strip_name in active_strips else resting_color
        fill_strip(ctx, strip_name, color)