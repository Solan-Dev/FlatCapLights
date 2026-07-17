from .green_cycle import render as render_green_cycle
from .ten_segment_colors import render as render_ten_segment_colors
from .comet import render as render_comet
from .diagnostic_blocks import render as render_diagnostic_blocks
from .rainbow_sweep import render as render_rainbow_sweep
from .breathing_color import render as render_breathing_color
from .meteor_shower import render as render_meteor_shower
from .twinkle_field import render as render_twinkle_field
from .color_wipe import render as render_color_wipe
from .theater_chase import render as render_theater_chase
from .larson_scanner import render as render_larson_scanner
from .aurora import render as render_aurora
from .pulse_train import render as render_pulse_train
from .confetti import render as render_confetti


# Canonical pattern registry: one name maps to one pattern function.
PATTERNS = {
    "comet": render_comet,
    "green_cycle": render_green_cycle,
    "ten_segment_colors": render_ten_segment_colors,
    "diagnostic_blocks": render_diagnostic_blocks,
    "rainbow_sweep": render_rainbow_sweep,
    "breathing_color": render_breathing_color,
    "meteor_shower": render_meteor_shower,
    "twinkle_field": render_twinkle_field,
    "color_wipe": render_color_wipe,
    "theater_chase": render_theater_chase,
    "larson_scanner": render_larson_scanner,
    "aurora": render_aurora,
    "pulse_train": render_pulse_train,
    "confetti": render_confetti,
}
