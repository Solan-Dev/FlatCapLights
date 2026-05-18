from .green_cycle import render as render_green_cycle
from .ten_segment_colors import render as render_ten_segment_colors
from .comet import render as render_comet


# Canonical pattern registry: one name maps to one pattern function.
PATTERNS = {
    "comet": render_comet,
    "green_cycle": render_green_cycle,
    "ten_segment_colors": render_ten_segment_colors,
}
