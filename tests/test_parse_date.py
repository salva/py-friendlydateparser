import pytest
from friendlydateparser import parse_date
from datetime import datetime, timedelta

now = "2023-10-12"
dates = [
    ("january/1/2017", "2017-01-01", "OK"),
    ("february/14/2017", "2017-02-14", "OK"),
    ("march/15/2017", "2017-03-15", "OK"),
    ("april/30/2017", "2017-04-30", "OK"),
    ("may/5/2017", "2017-05-05", "OK"),
    ("june/21/2017", "2017-06-21", "OK"),
    ("july/4/2017", "2017-07-04", "OK"),
    ("august/15/2017", "2017-08-15", "OK"),
    ("september/9/2017", "2017-09-09", "OK"),
    ("october/3/2017", "2017-10-03", "OK"),
    ("november/11/2017", "2017-11-11", "OK"),
    ("december/25/2017", "2017-12-25", "OK"),
    ("3/january/2017", "2017-01-03", "OK"),
    ("14/february/2017", "2017-02-14", "OK"),
    ("15/march/2017", "2017-03-15", "OK"),
    ("30/april/2017", "2017-04-30", "OK"),
    ("5/may/2017", "2017-05-05", "OK"),
    ("21/june/2017", "2017-06-21", "OK"),
    ("4/july/2017", "2017-07-04", "OK"),
    ("15/august/2017", "2017-08-15", "OK"),
    ("9/september/2017", "2017-09-09", "OK"),
    ("3/october/2017", "2017-10-03", "OK"),
    ("11/november/2017", "2017-11-11", "OK"),
    ("25/december/2017", "2017-12-25", "OK"),
    ("10/3/2017", "2017-10-03", "OK"),
    ("the 3rd of october, 2017", "2017-10-03", "OK"),
    ("the 3rd of october 2017", "2017-10-03", "OK"),
    ("10/1045", "1045-10-01", "OK"),
    ("october/2017", "2017-10-01", "OK"),
    ("10/2017", "2017-10-01", "OK"),
    ("2017", "2017-01-01", "OK"),
    ("october 2017", "2017-10-01", "OK"),
    ("january/2023", "2023-01-01", "OK"),
    ("february/2023", "2023-02-01", "OK"),
    ("march/2023", "2023-03-01", "OK"),
    ("april/2023", "2023-04-01", "OK"),
    ("may/2023", "2023-05-01", "OK"),
    ("june/2023", "2023-06-01", "OK"),
    ("july/2023", "2023-07-01", "OK"),
    ("august/2023", "2023-08-01", "OK"),
    ("september/2023", "2023-09-01", "OK"),
    ("october/3", "2023-10-03", "OK"),
    ("3/october", "2023-10-03", "OK"),
    ("10/3", "2023-10-03", "OK"),
    ("the 3rd of october", "2023-10-03", "OK"),
    ("october", "2023-10-01", "OK"),
    ("last sunday", "2023-10-08", "TODO"),
    ("next monday", "2023-10-16", "TODO"),
    ("next friday", "2023-10-20", "TODO"),
    ("last tuesday", "2023-10-10", "TODO"),
    ("next tue", "2023-10-17", "TODO"),
    ("1/january", "2023-01-01", "OK"),
    ("31/december", "2023-12-31", "OK"),
    ("15/july", "2023-07-15", "OK"),
    ("4/april", "2023-04-04", "OK"),
    ("29/february/2020", "2020-02-29", "OK"),  # Leap year
    ("february/29/2020", "2020-02-29", "OK"),  # Leap year
    ("march", "2023-03-01", "OK"),  # Incomplete date (month only)
    ("15", ValueError, "OK")  # Incomplete date (day only)
]

times = [
    ("14:30", "14:30:00.000000", "OK"),
    ("2:45 PM", "14:45:00.000000", "OK"),
    ("11:59 PM", "23:59:00.000000", "OK"),
    ("00:00", "00:00:00.000000", "OK"),
    ("midnight", "00:00:00.000000", "OK"),
    ("noon", "12:00:00.000000", "OK"),
    ("midday", "12:00:00.000000", "OK"),
    ("6:00 AM", "06:00:00.000000", "OK"),
    ("23:15", "23:15:00.000000", "OK"),
    ("7:45 pm", "19:45:00.000000", "OK"),
    ("5 o'clock in the evening", "17:00:00.000000", "TODO"),
    ("quarter past three", "15:15:00.000000", "TODO"),
    ("half past ten", "10:30:00.000000", "TODO"),
    ("ten to five", "16:50:00.000000", "TODO"),
    ("24:45", ValueError, "OK"),  # Invalid time representation
    ("12:13 PM", "12:13:00.000000", "OK"),
    ("12:13 AM", "00:13:00.000000", "OK"),
    ("2h 45m", "02:45:00.000000", "OK"),  # Alternative time format
    ("1:30:45.1 PM", "13:30:45.100000", "OK"),  # Time with seconds and microseconds
    ("3h", "03:00:00.000000", "OK"),  # Hours only
    ("12h 30min 0.65seconds", "12:30:00.650000", "OK"),  # Alternative format with hours and minutes and microseconds
    ("2h15min30.9s", "02:15:30.900000", "OK")  # Alternative format with hours, minutes, seconds, and microseconds
]

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
    ("2999 at 3:00:00.000000", "2999-01-01T03:00:00.000000", "OK")
]

@pytest.mark.parametrize("input_text, expected, tag", dates)
def test_dates(input_text, expected, tag):
    if tag == "TODO":
        pytest.xfail(reason="Marked as TODO")

    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            parse_date(input_text, now=now)
    else:
        result = parse_date(input_text, now=now)
        result = result.strftime('%Y-%m-%d')
        assert result == expected, f"Wrong parsed date, input: '{input_text}', parsed: '{result}', expected: '{expected}'"


