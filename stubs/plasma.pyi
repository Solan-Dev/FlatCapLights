COLOR_ORDER_RGB: int
COLOR_ORDER_RBG: int
COLOR_ORDER_GRB: int
COLOR_ORDER_GBR: int
COLOR_ORDER_BRG: int
COLOR_ORDER_BGR: int

class WS2812:
    def __init__(self, num_leds: int, *, color_order: int = ...) -> None: ...
    def start(self, fps: int) -> None: ...
    def set_rgb(self, index: int, red: int, green: int, blue: int) -> None: ...
