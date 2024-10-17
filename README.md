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

### `parse_time(text)`

Extracts time information from a given string and returns a time
object. This function is suitable for parsing times like "2:45 PM",
"14:30", "midnight", etc.

- **Parameters**:
  - `text` (str): The text containing time information to be parsed.

- **Returns**: A `datetime.time` object.

- **Example**:
  ```python
  time_obj = parse_time("2:45 PM")
  # Returns: datetime.time(14, 45)
  ```

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

### `parse_datetime(text, now=None, month_first=True)`

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

- **Returns**: A `datetime.datetime` object.

- **Example**:
  ```python
  datetime_obj = parse_datetime("january 1, 2017 at 14:30")
  # Returns: datetime.datetime(2017, 1, 1, 14, 30)
  ```

## Supported Formats

The module can parse a wide variety of date and time formats,
including but not limited to:

- **Explicit Dates**: Formats such as `3-october-2017`, `10/3/2017`,
  `2017/12/3`, `march 15, 2017`, `15/july/2023` are accepted, with the
  ability to handle both `mm/dd/yyyy` and `dd/mm/yyyy` formats based
  on the `month_first` parameter.

- **Incomplete dates**: `1 october`, `10/3`, `feb 2020`, `2024`,
  `nov`. The current year is used to fill the missing data by the
  right and "ones" or "zeros" by the left. For instance, `feb 2020`
  becomes the 1st of febrery of 2020 at 00:00:00, `october` becomes
  the 1st of october of the current year at 00:00:00. Note that very
  ambiguous expressions as `9` are just rejected.

- **Relative Dates**: `the first of next month`, `next week`, `the day
  after tomorrow`, `october 1 last year`.

- **Relative Weekdays**: Phrases like `monday next week`, `last
  monday`, `second sunday of 2023`, `last friday of october`.

- **Year and month week numbers**: `wed week 20 2018`, `week 2 october
  2017`, `last week october`.

- **Time and Timezones**: `today at 12pm`, `last monday 12h40m`,
  `10/2/2022 40:30:12.1 CEST`, `tomorrow at midnight Europe/Paris`.

- **Before and after**: `3 weeks before yesterday`, `1d 4h after next
  monday at noon`, `1 month ago`. Time units can be abbreviated, for
  instance, both `days`, `day`, `ds` and `d` are accepted as days. On
  the other hand months can only be given as `month` or `months` as
  `m` and `ms` mean minutes.

- **ISO8601**: `2024-12-31T13:01+02:00`, `2024-W01-8T10:12Z`,
  `2008-365`.

The module supports both common formats like `mm/dd/yyyy` and
`dd/mm/yyyy`, with the ability to distinguish based on the
`month_first` parameter.

**Note: If you think a new format should be supported, just ask for
it!**

## Error Handling

- If the input text is incomplete or not recognizable as a valid
  date/time, a `ValueError` may be raised.

## Example Usage

```python
from friendlydateparser import parse_date, parse_time, parse_datetime

# Parsing a date
date_obj = parse_date("the last day of next jan")
# Returns: datetime.date(2024, 1, 31)

# Parsing a time
time_obj = parse_time("2:00 PM")
# Returns: datetime.time(14, 0)

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
