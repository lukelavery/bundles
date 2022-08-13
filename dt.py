from datetime import date


def short_string_to_date(shortfmt):
    # handle error
    year = int(shortfmt[:4])
    month = int(shortfmt[5:7])
    day = int(shortfmt[8:])
    d = date(year, month, day)
    return d


def date_to_long_string(d):
    long_string = d.strftime("%d %B %Y")
    return long_string


def short_string_to_long_string(shortfmt):
    d = short_string_to_date(shortfmt)
    longfmt = date_to_long_string(d)
    return longfmt
