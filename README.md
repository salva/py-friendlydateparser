# friendlydateparser

This Python module provides methods for parsing text into date, and
datetime objects.

For instance, it can parse expressions like:

    tuesday, october 15, 2024 14:45 Europe/Paris
    2 days before the last day of next month
    1h15m after next sunday at midnight CEST
    the second monday of 2012

The aim is to be able to accept expressions witch, even if complex,
express date references which are common in everyday life.

## API

### `parse_date(text, now=None, month_first=True)`

Parses date information from a given string and returns a date
object. The function can handle different formats including relative
date descriptions (e.g., "next month", "last Friday") or explicit
dates (e.g., "10/3/2017", "15th of July").

- **Parameters**:
  - `text` (str): The text containing date information to be parsed.
  - `now` (datetime.date or datetime.datetime, optional): The
      reference date to use for relative expressions. Defaults to the
      current date if not specified.
  - `month_first` (bool, optional): Indicates whether the month
      appears first in numerical dates (e.g., `10/3` is treated as
      October 3rd if `month_first=True`). Defaults to `True`.

- **Returns**: A `datetime.date` object.

- **Example**:
  ```python
  date_obj = parse_date("the first of next month")
  # Assuming today is 2023-10-10, returns: datetime.date(2023, 11, 1)
  ```

### `parse_datetime(text, now=None, month_first=True, default_tz=None)`

Parses both date and time information from a given string and returns
a datetime object. The function handles a wide range of date and time
formats, including explicit and relative formats.

- **Parameters**:
  - `text` (str): The text containing datetime information to be parsed.
  - `now` (datetime.date or datetime.datetime, optional): The
      reference date to use for relative expressions. Defaults to the
      current date and time if not specified.
  - `month_first` (bool, optional): Indicates whether the month
      appears first in numerical dates (e.g., `10/3` is treated as
      October 3rd if `month_first=True`). Defaults to `True`.
  - `default_tz`: default timezone when the given string doesn't
    specify one. Defaults to None which causes the function to return a
    [naive](https://docs.python.org/3/library/datetime.html#aware-and-naive-objects)
    datetime object when a TZ does not appear explicitly in the given
    text.

- **Returns**: A `datetime.datetime` object.

- **Example**:
  ```python
  datetime_obj = parse_datetime("january 1, 2017 at 14:30")
  # Returns: datetime.datetime(2017, 1, 1, 14, 30)
  ```


## Supported Formats

The module can parse a wide variety of date and time formats, such as:

- **Explicit Dates**: Formats such as `3-october-2017`, `10/3/2017`,
  `2017/12/3`, `march 15, 2017`, `15/july/2023` are accepted, with the
  ability to handle both `mm/dd/yyyy` and `dd/mm/yyyy` formats based
  on the `month_first` parameter.

- **Incomplete dates**: `1 october`, `10/3`, `feb 2020`, `2024`,
  `nov`. The current year is used to fill in missing information on
  the right, while missing values on the left are filled with "ones"
  or "zeros" as appropriate. For instance, `feb 2020` becomes the 1st
  of February of 2020 at 00:00:00, `october` becomes the 1st of
  October of the current year at 00:00:00.

  Note that very ambiguous expressions like `9` are just rejected.

- **Relative Dates**: `the first of next month`, `next week`, `the day
  after tomorrow`, `october 1 last year`.

- **Relative Weekdays**: Phrases like `monday next week`, `last
  monday`, `second sunday of 2023`, `last friday of october`.

- **Year and month week numbers**: `wed week 20 2018`, `week 2 october
  2017`, `last week october`.

- **Time and Timezones**: `today at 12pm`, `last monday 12h40m`,
  `10/2/2022 40:30:12.1 CEST`, `tomorrow at midnight Europe/Paris`.

- **Deltas (before and after)**: `3 weeks before yesterday`, `1d 4h
  after next monday at noon`, `1 month ago`. Time units can be
  abbreviated, for instance, both `days`, `day`, `ds` and `d` are
  accepted as days. On the other hand months can only be given as
  `month` or `months` as `m` and `ms` mean minutes.

  Negative numbers are also accepted: `3 weeks -1 day before today`.

- **Relative references (by)**: in some cases it is useful to
  reference some relative date from another date. For instance, a
  common case is when you want to express an idea like "the last
  Monday including today if today is Monday". We can express that with
  by as `last monday by tomorrow`. Other examples are `this month by
  sunday`, `monday by the first of next month`.

- [**ISO8601**](https://en.wikipedia.org/wiki/ISO_8601):
  `2024-12-31T13:01+02:00`, `2024-W01-8T10:12Z`, `2008-365`.

And some extra considerations:

- The only inflexible rule when parsing is the order of the
  components, which must follow *(delta, date, time, timezone)*.

- Besides that, the module tries to parse anything which makes sense
  without being ambiguous.

- Common particles such as `the`, `of`, commas, dashes,
  slashes, etc. can be included when they are common but also usually
  excluded. For instance, `october the second of 2015`, `october the
  second, 2015`, `october 2nd 2015` are all parsed correctly.

- Space can be included freely everywhere except:
  - Between the digits of a number.
  - In ordinal numbers composed by several words (dashes must be
    used to join them as in `twenty-third`).
  - In timezone names (`Europe/Paris`).

  For instance, valid expressions are `1d-1h before october/23`, `1
  d - 1 h before october / 23`.

  On the other hand, space is required between consecutive words. For
  instance, `fridaynextweek` is not a valid expression.

- Abbreviations for weekdays, month names and units are accepted as
  long as they are unambiguous.

- Ordinals can be written as numbers with the appropriate suffix (1st,
  25th, etc.). Ordinals from 1st to 99th can also be written as words.


**Note: If you think a new format should be supported, just ask for
it!**

## Error Handling

- If the input text is incomplete or not recognizable as a valid
  date/time, a `ValueError` may be raised.

## Example Usage

```python
from friendlydateparser import parse_date, parse_datetime

# Parsing a date
date_obj = parse_date("the last day of next jan")
# Returns: datetime.date(2024, 1, 31)

# Parsing a datetime
datetime_obj = parse_datetime("march 15, 2017 11:59 PM")
# Returns: datetime.datetime(2017, 3, 15, 23, 59)
```

## See Also

- [`datetime`](https://docs.python.org/3/library/datetime.html): For
  working with date and time objects in Python.

- [`time`](https://docs.python.org/3/library/time.html): Provides
  various time-related functions, such as working with timestamps or
  sleep functions. This can be useful in combination with date and
  time parsing.

- [`dateutil.relativedelta`](https://dateutil.readthedocs.io/en/stable/relativedelta.html):
  For relative date calculations, like adding or subtracting months or
  years.

- [`calendar`](https://docs.python.org/3/library/calendar.html): For
  calendar-related functions, such as determining leap years or
  getting the number of days in a month.

- [`pytz`](https://pypi.org/project/pytz/): For handling time zones in
  Python. It can be useful when parsing dates and times that involve
  different time zones or when converting between local times and UTC.

- [`pendulum`](https://pendulum.eustace.io/): A library that provides
  easy-to-use functions for parsing, formatting, and manipulating
  dates and times, with a focus on improved datetime management and
  natural language parsing.

- [`dateparser`](https://dateparser.readthedocs.io/en/latest/): A
  library similar to this module, which parses natural language
  dates, even supporting multiple languages.

- [`Arrow`](https://arrow.readthedocs.io/en/latest/): A `datetime`
  alternative with a focus on usability. The
  [`dehumanize`](https://arrow.readthedocs.io/en/latest/guide.html#dehumanize)
  feature allows one to parse time deltas expressed in natural
  language.

## License

Copyright (c) 2024 Salvador Fandiño García

This project is licensed under the MIT License. See the `LICENSE` file for more details.
