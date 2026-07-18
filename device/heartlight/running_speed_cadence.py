def decode_measurement(data):
    """Decode a Bluetooth Running Speed and Cadence Measurement notification."""
    if len(data) < 4:
        raise ValueError("Truncated running speed and cadence measurement")

    flags = data[0]
    speed_mps = (data[1] | (data[2] << 8)) / 256.0
    cadence_spm = data[3]
    index = 4

    stride_length_m = None
    if flags & 0x01:
        if len(data) < index + 2:
            raise ValueError("Truncated stride length")
        stride_length_m = (data[index] | (data[index + 1] << 8)) / 100.0
        index += 2

    total_distance_m = None
    if flags & 0x02:
        if len(data) < index + 4:
            raise ValueError("Truncated total distance")
        total_distance_m = (
            data[index]
            | (data[index + 1] << 8)
            | (data[index + 2] << 16)
            | (data[index + 3] << 24)
        ) / 10.0
        index += 4

    if index != len(data):
        raise ValueError("Unexpected running speed and cadence data")
    return cadence_spm, speed_mps, stride_length_m, total_distance_m