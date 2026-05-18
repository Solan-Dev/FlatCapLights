# Validate strip definitions against total LED count.
def validate_strip_defs(strip_defs, led_count, strict_layout=True):
    if not isinstance(strip_defs, dict) or not strip_defs:
        raise ValueError("STRIP_DEFS must be a non-empty dictionary")

    used = [False] * max(0, int(led_count))

    for strip_name, definition in strip_defs.items():
        if not isinstance(definition, dict):
            raise ValueError("Invalid strip definition for {}".format(strip_name))

        if "start" not in definition or "length" not in definition:
            raise ValueError("Missing start/length for {}".format(strip_name))

        start = int(definition["start"])
        length = int(definition["length"])

        if length <= 0:
            raise ValueError("Strip length must be > 0 for {}".format(strip_name))

        end = start + length
        if start < 0 or end > led_count:
            raise ValueError("Strip out of range for {}".format(strip_name))

        for index in range(start, end):
            if used[index]:
                if strict_layout:
                    raise ValueError("Strip overlap at LED {} ({})".format(index, strip_name))
                break
        else:
            for index in range(start, end):
                used[index] = True


# Return configured strip length.
def strip_length(strip_defs, strip_name):
    return int(strip_defs[strip_name]["length"])


# Convert strip-local index to global LED index.
def strip_local_to_global(strip_defs, strip_name, local_index):
    definition = strip_defs[strip_name]
    start = int(definition["start"])
    length = int(definition["length"])
    reversed_strip = bool(definition.get("reversed", False))

    if local_index < 0 or local_index >= length:
        raise IndexError("Local index out of range for {}".format(strip_name))

    if reversed_strip:
        return start + (length - 1 - local_index)

    return start + local_index


# Validate optional logical segment defs that slice physical strips.
def validate_pattern_segments(segment_defs, strip_defs):
    if not isinstance(segment_defs, dict):
        raise ValueError("segment_defs must be a dictionary")

    for segment_name, definition in segment_defs.items():
        if not isinstance(definition, dict):
            raise ValueError("Invalid segment definition for {}".format(segment_name))

        strip_name = definition.get("strip")
        if strip_name not in strip_defs:
            raise ValueError("Unknown strip {} for {}".format(strip_name, segment_name))

        if "start" not in definition or "length" not in definition:
            raise ValueError("Missing start/length for {}".format(segment_name))

        start = int(definition["start"])
        length = int(definition["length"])

        if length <= 0:
            raise ValueError("Segment length must be > 0 for {}".format(segment_name))

        strip_len = strip_length(strip_defs, strip_name)
        if start < 0 or (start + length) > strip_len:
            raise ValueError("Segment out of strip range for {}".format(segment_name))


# Resolve logical segment-local index to global LED index.
def segment_local_to_global(segment_defs, strip_defs, segment_name, local_index):
    definition = segment_defs[segment_name]
    strip_name = definition["strip"]
    start = int(definition["start"])
    length = int(definition["length"])
    reversed_segment = bool(definition.get("reversed", False))

    if local_index < 0 or local_index >= length:
        raise IndexError("Local index out of range for {}".format(segment_name))

    segment_offset = local_index
    if reversed_segment:
        segment_offset = length - 1 - local_index

    return strip_local_to_global(strip_defs, strip_name, start + segment_offset)
