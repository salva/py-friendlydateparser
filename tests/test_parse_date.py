import pytest
from friendlydateparser import parse_date
from datetime import datetime, timedelta

now = "2023-10-12"
dates = [
    ("the first of next month", "2023-11-01", "OK"),
    ("the first of january next year", "2024-01-01", "OK"),
    ("the first of last month", "2023-09-01", "OK"),
    ("the first of october, last year", "2022-10-01", "OK"),
    ("monday", "2023-10-09", "OK"),
    ("next month", "2023-11-01", "OK"),
    ("next year", "2024-01-01", "OK"),
    ("last month", "2023-09-01", "OK"),
    ("last year", "2022-01-01", "OK"),
    ("monday next week", "2023-10-16", "OK"),
    ("next week", "2023-10-16", "OK"),
    ("last week", "2023-10-02", "OK"),
    ("this comming friday", "2023-10-13", "OK"),
    ("last friday", "2023-10-06", "OK"),
    ("last monday", "2023-10-09", "OK"),
    ("the day after tomorrow", "2023-10-14", "OK"),
    ("the day before yesterday", "2023-10-10", "OK"),
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
    ("mon, 10/3/2017", ValueError, "OK"),
    ("tuesday 10/3/2017", "2017-10-03", "OK"),
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
    ("15", ValueError, "OK"),  # Incomplete date (day only)
    ("last day of 2023", "2023-12-31", "OK"),
    ("last day of february 2023", "2023-02-28", "OK"),
    ("the last day of jan 2020", "2020-01-31", "OK"),
    ("the last day of jan", "2023-01-31", "OK"),
    ("the last day of next jan", "2024-01-31", "OK"),
    ("the last day of next jan by october 2020", "2021-01-31", "OK"),
    ("sunday week 1 2012", "2012-01-08", "OK"),
    ("monday week 4 april 2023", "2023-04-24", "OK"),
    ("wednesday week 2 march 2020", "2020-03-11", "OK"),
    ("week 3 june", "2023-06-12", "OK"),
    ("monday week 45 2019", "2019-11-04", "OK"),
    ("monday week 5 7/2019", ValueError, "OK"),
    ("last week of 2029", "2029-12-24", "OK"),
    ("last week of jan 2029", "2029-01-22", "OK"),
    ("friday week 5 september", ValueError, "OK"), # Out of range week number
    ("week 55 2023", ValueError, "OK"),  # Out of range week number
    ("sunday week 54 2021", ValueError, "OK"),  # Out of range week number for year 2021
    ("week 0 april 2023", ValueError, "OK"),  # Invalid week number (zero)
    ("second sunday of 2023", "2023-01-08", "OK"),
    ("second sunday of january 2023", "2023-01-08", "OK"),
    ("131st day of 2023", "2023-05-11", "OK"),
    ("last sunday of 2020", "2020-12-27", "OK"),
    ("last monday oct/2024", "2024-10-28", "OK"),
    ("last monday of october next year", "2024-10-28", "OK"),
    ("last day of last year", "2022-12-31", "OK"),
    ("2nd tuesday of next year", "2024-01-09", "OK"),
    ("2nd saturday next september", "2024-09-14", "OK"),
    ("3rd sunday this year", "2023-01-15", "OK"),
    ("wed week 2 april last year", "2022-04-13", "OK"),
    ("3 days before the last week of 2012", "2012-12-21", "OK"),
    ("1 month after january 30", "2023-02-28", "OK"),
    ("2 weeks -1d before 2023-10-12", "2023-09-29", "OK"),
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


