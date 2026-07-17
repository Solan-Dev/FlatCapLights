def clamp(value, low, high):
    if value < low:
        return low
    if value > high:
        return high
    return value


def hsv_to_rgb(hue, saturation, value):
    hue = hue % 1.0
    saturation = clamp(saturation, 0.0, 1.0)
    value = clamp(value, 0.0, 1.0)
    sector = int(hue * 6.0)
    fraction = hue * 6.0 - sector
    low = value * (1.0 - saturation)
    descending = value * (1.0 - fraction * saturation)
    ascending = value * (1.0 - (1.0 - fraction) * saturation)
    sector %= 6

    if sector == 0:
        red, green, blue = value, ascending, low
    elif sector == 1:
        red, green, blue = descending, value, low
    elif sector == 2:
        red, green, blue = low, value, ascending
    elif sector == 3:
        red, green, blue = low, descending, value
    elif sector == 4:
        red, green, blue = ascending, low, value
    else:
        red, green, blue = value, low, descending

    return int(red * 255), int(green * 255), int(blue * 255)


def scaled_hsv(hue, saturation, value, brightness):
    red, green, blue = hsv_to_rgb(hue, saturation, value * brightness)
    return red, green, blue