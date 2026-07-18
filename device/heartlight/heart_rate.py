def decode_measurement(data):
    """Decode a Bluetooth Heart Rate Measurement notification."""
    if not data:
        raise ValueError("Empty heart-rate notification")

    flags = data[0]
    index = 1
    if flags & 0x01:
        if len(data) < index + 2:
            raise ValueError("Truncated 16-bit heart rate")
        bpm = data[index] | (data[index + 1] << 8)
        index += 2
    else:
        if len(data) < index + 1:
            raise ValueError("Truncated 8-bit heart rate")
        bpm = data[index]
        index += 1

    if flags & 0x08:
        if len(data) < index + 2:
            raise ValueError("Truncated energy expended")
        index += 2

    rr_intervals = []
    if flags & 0x10:
        while index + 1 < len(data):
            rr_value = data[index] | (data[index + 1] << 8)
            rr_intervals.append(rr_value / 1024.0)
            index += 2
        if index != len(data):
            raise ValueError("Truncated RR interval")

    if bpm <= 0:
        raise ValueError("Invalid heart rate")
    return bpm, tuple(rr_intervals)