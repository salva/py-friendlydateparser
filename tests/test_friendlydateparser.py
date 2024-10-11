import pytest
from friendlydateparser import parse_date, parse_time, parse_datetime
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
    ("february/29/2020", "2020-02-29", "OK")   # Leap year
]

times = [
    ("14:30", "14:30:00", "OK"),
    ("2:45 PM", "14:45:00", "OK"),
    ("11:59 PM", "23:59:00", "OK"),
    ("11:59:04.02 PM", "23:59:04.02", "OK"),
    ("00:00", "00:00:00", "OK"),
    ("midnight", "00:00:00", "OK"),
    ("noon", "12:00:00", "OK"),
    ("midday", "12:00:00", "OK"),
    ("6:00 AM", "06:00:00", "OK"),
    ("23:15", "23:15:00", "OK"),
    ("7:45 pm", "19:45:00", "OK"),
    ("5 o'clock in the evening", "17:00:00", "TODO"),
    ("quarter past three", "15:15:00", "TODO"),
    ("half past ten", "10:30:00", "TODO"),
    ("ten to five", "16:50:00", "TODO"),
    ("24:45", ValueError, "OK"),  # Invalid time representation
    ("12:13 PM", "12:13:00", "OK"),
    ("12:13 AM", "00:13:00", "OK")
]

datetimes = [
    ("january 1, 2017 at 14:30", "2017-01-01T14:30:00", "OK"),
    ("february 14, 2017 at 2:45 PM", "2017-02-14T14:45:00", "OK"),
    ("march 15, 2017 11:59 PM", "2017-03-15T23:59:00", "OK"),
    ("april 30, 2017 00:00", "2017-04-30T00:00:00", "OK"),
    ("may 5, 2017 noon", "2017-05-05T12:00:00", "OK"),
    ("june 21, 2017 at 6:00 AM", "2017-06-21T06:00:00", "OK"),
    ("july 4, 2017 at 23:15", "2017-07-04T23:15:00", "OK"),
    ("august 15, 2017 at 7:45 pm", "2017-08-15T19:45:00", "OK"),
    ("december 25, 2017 at 12:13 PM", "2017-12-25T12:13:00", "OK"),
    ("december 25, 2017 at 12:13 AM", "2017-12-25T00:13:00", "OK"),
    ("march 2017 at 2:00 PM", "2017-03-01T14:00:00", "OK"),  # Incomplete date with time
    ("2017 at 4:15", "2017-01-01T04:15:00", "OK"),  # Year with time only
    ("january 1, 2017 at 12h30min", "2017-01-01T12:30:00", "OK"),  # Date with alternative time format
    ("february 14, 2017 at 3h15min30s", "2017-02-14T03:15:30", "OK"),  # Date with hours, minutes, and seconds
    ("march 15, 2017 at midnight", "2017-03-15T00:00:00", "OK"),  # Date with 'midnight'
    ("april 30, 2017 at noon", "2017-04-30T12:00:00", "OK"),  # Date with 'noon'
    ("may 5, 2017 at 5 o'clock in the evening", "2017-05-05T17:00:00", "TODO"),  # Date with informal time expression
    ("june 21, 2017 at quarter past three", "2017-06-21T15:15:00", "TODO"),  # Date with informal time expression
    ("july 4, 2017 at half past ten", "2017-07-04T10:30:00", "TODO"),  # Date with informal time expression
    ("august 15, 2017 at ten to five", "2017-08-15T16:50:00", "TODO")  # Date with informal time expression
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

@pytest.mark.parametrize("input_text, expected, tag", times)
def test_times(input_text, expected, tag):
    if tag == "TODO":
        pytest.xfail(reason="Marked as TODO")

    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            parse_time(input_text)
    else:
        result = parse_time(input_text)
        result = result.strftime('%H:%M:%S')
        assert result == expected, f"Wrong parsed time, input: '{input_text}', parsed: '{result}', expected: '{expected}'"

@pytest.mark.parametrize("input_text, expected, tag", datetimes)
def test_datetimes(input_text, expected, tag):
    if tag == "TODO":
        pytest.xfail(reason="Marked as TODO")

    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            parse_datetime(input_text)
    else:
        result = parse_datetime(input_text)
        result = result.strftime('%Y-%m-%dT%H:%M:%S')
        assert result == expected, f"Wrong parsed datetime, input: '{input_text}', parsed: '{result}', expected: '{expected}'"
