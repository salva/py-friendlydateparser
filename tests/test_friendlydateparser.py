import pytest
from friendlydateparser import parse_date
from datetime import datetime, timedelta

now = "2023-10-12"
inputs = [
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

@pytest.mark.parametrize("input_text, expected, tag", inputs)
def test_parser(input_text, expected, tag):
    if tag == "TODO":
        pytest.xfail(reason="Marked as TODO")

    if isinstance(expected, Exception):
        with pytest.raises(expected):
            parse_date(input_text, now=now)
    else:
        result = parse_date(input_text, now=now)
        if isinstance(result, datetime):
            result = result.strftime('%Y-%m-%d')
        assert result == expected, f"Failed to parse input: '{input_text}'"

