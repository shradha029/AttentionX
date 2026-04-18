def to_seconds(time_input):
    """
    Accepts:
    - int (already seconds)
    - "HH:MM:SS"
    Returns seconds (int)
    """

    if isinstance(time_input, int):
        return time_input

    if isinstance(time_input, str):
        parts = list(map(int, time_input.split(":")))
        if len(parts) == 3:
            h, m, s = parts
            return h*3600 + m*60 + s
        elif len(parts) == 2:
            m, s = parts
            return m*60 + s

    raise ValueError("Invalid time format")