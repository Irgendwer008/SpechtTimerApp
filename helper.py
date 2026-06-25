def format_time(t: float, time_diff: bool = False):
    if t is None:
        return "--:--.---"

    t = round(t, 3)

    sign = ""

    if t >= 0:
        if time_diff:
            sign = "+"
    else:
        sign = "-"

    minutes = int(abs(t) // 60)
    seconds = abs(t) % 60

    return f"{sign}{minutes:02d}:{seconds:06.3f}"