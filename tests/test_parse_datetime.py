import pytest
from friendlydateparser import parse_datetime
from datetime import datetime, timedelta, timezone

now = "2023-10-12"

datetimes = [
    ("january 1, 2017 at 14:30", "2017-01-01T14:30:00.000000", "OK"),
    ("february 14, 2017 at 2:45:00.654 PM", "2017-02-14T14:45:00.654000", "OK"),
    ("march 15, 2017 11:59:00.78 PM", "2017-03-15T23:59:00.780000", "OK"),
    ("april 30, 2017 00:00", "2017-04-30T00:00:00.000000", "OK"),
    ("may 5, 2017 noon", "2017-05-05T12:00:00.000000", "OK"),
    ("june 21, 2017 at 6:00:00.2 AM", "2017-06-21T06:00:00.200000", "OK"),
    ("july 4, 2017 at 23:15", "2017-07-04T23:15:00.000000", "OK"),
    ("august 15, 2017 at 7:45:00.444 pm", "2017-08-15T19:45:00.444000", "OK"),
    ("december 25, 2017 at 12:13:00.555 PM", "2017-12-25T12:13:00.555000", "OK"),
    ("december 25, 2017 at 12:13 AM", "2017-12-25T00:13:00.000000", "OK"),
    ("march 2017 at 2:00:00.7 PM", "2017-03-01T14:00:00.700000", "OK"),
    ("march 31", "2023-03-31T00:00:00.000000", "OK"),
    ("october 2020", "2020-10-01T00:00:00.000000", "OK"),
    ("jul 3rd at noon", "2023-07-03T12:00:00.000000", "OK"),
    ("2999 at 3:00:00.000000", "2999-01-01T03:00:00.000000", "OK"),
    ("2h ago", "2023-10-11T22:00:00.000000", "OK"),
    ("1h 1s ago", "2023-10-11T22:59:59.000000", "OK"),
    ("1h -1s ago", "2023-10-11T23:00:01.000000", "OK"),
    ("1h 0.1s ago", "2023-10-11T22:59:59.900000", "OK"),
    ("1h -0.1s ago", "2023-10-11T23:00:00.100000", "OK"),
    ("2 days after today at 1:00pm CEST", "2023-10-14T11:00:00.000000", "OK"),
    ("1 october 12:00 EST", "2023-10-01T17:00:00.000000", "OK"),
]

@pytest.mark.parametrize("input_text, expected, tag", datetimes)
def test_datetimes(input_text, expected, tag):
    if tag == "TODO":
        pytest.xfail(reason="Marked as TODO")

    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            parse_datetime(input_text, now=now)
    else:
        result = parse_datetime(input_text, now=now, default_tz='UTC')
        result = result.astimezone(timezone.utc)

        result = result.strftime('%Y-%m-%dT%H:%M:%S.%f')
        assert result == expected, f"Wrong parsed datetime, input: '{input_text}', parsed: '{result}', expected: '{expected}'"
