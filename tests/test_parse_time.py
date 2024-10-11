import pytest
from friendlydateparser import parse_time
from datetime import datetime, timedelta

now = "2023-10-12"
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

@pytest.mark.parametrize("input_text, expected, tag", times)
def test_times(input_text, expected, tag):
    if tag == "TODO":
        pytest.xfail(reason="Marked as TODO")

    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            parse_time(input_text)
    else:
        result = parse_time(input_text)
        result = result.strftime('%H:%M:%S.%f')
        assert result == expected, f"Wrong parsed time, input: '{input_text}', parsed: '{result}', expected: '{expected}'"
