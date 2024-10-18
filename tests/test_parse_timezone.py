import pytest
from friendlydateparser import parse_datetime
from datetime import datetime, timedelta, timezone

now = "2023-10-12"

datetimes = [
    ("january 1, 2017 at 14:30", None, "2017-01-01T14:30:00.000000", "OK"),
    ("january 1, 2017 at 14:30", 'CEST', "2017-01-01T12:30:00.000000", "OK"),
    ("february 14, 2017 at 2:45:00.654 PM", 'Z', "2017-02-14T14:45:00.654000", "OK"),
]

@pytest.mark.parametrize("input_text, default_tz, expected, tag", datetimes)
def test_datetimes(input_text, default_tz, expected, tag):
    if tag == "TODO":
        pytest.xfail(reason="Marked as TODO")

    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            parse_datetime(input_text, now=now)
    else:
        result = parse_datetime(input_text, now=now, default_tz=default_tz)
        if result.tzinfo is None:
            resultZ = result.replace(tzinfo=timezone.utc)
        else:
            resultZ = result.astimezone(timezone.utc)

        resultZ = resultZ.strftime('%Y-%m-%dT%H:%M:%S.%f')
        assert resultZ == expected, f"Wrong parsed datetime, input: '{input_text}', parsed: {result}, parsed TZ: {result.tzinfo}, parsedUTC: '{resultZ}', expected: '{expected}', default_tz: '{default_tz}'"
