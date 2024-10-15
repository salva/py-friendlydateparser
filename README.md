# friendlydateparser

This Python module provides three key methods for parsing text into
time, date, or datetime objects.

The aim is to be able to accept natural language date expressions
that, even if complex, are frequently used in everyday life.

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

- **Relative Dates**: Expressions like "the first of next month",
  "next week", "last Friday", "the day after tomorrow" are supported,
  allowing flexible parsing of commonly used phrases.

- **Explicit Dates**: Formats such as "10/3/2017", "march 15, 2017",
  "15/july/2023" are accepted, with the ability to handle both
  `mm/dd/yyyy` and `dd/mm/yyyy` formats based on the `month_first`
  parameter.

- **Relative Weekdays**: Phrases like "monday next week", "last
  monday", "second sunday of 2023" are parsed, allowing users to
  reference specific weekdays in relative terms.

- **Datetime Formats**: Full date and time expressions such as
  "january 1, 2017 at 14:30", "february 14, 2017 at 2:45 PM" are
  supported, making it easy to parse datetime values from text.

- **Special Terms**: Terms like "midnight", "noon" are also supported,
  allowing parsing of common time-related expressions.

- **Implicit Dates**: Natural expressions like "tomorrow at 5 PM",
  "next Monday", or "this month" are parsed effectively to
  provide accurate datetime objects.

- **Week Numbers**: References like "week 42 of 2023" can be parsed,
  providing an easy way to handle week-based scheduling.

- **Ordinal Dates**: Phrases like "the third of next month" or "the
  first Sunday in June" are supported, allowing flexibility with
  ordinal references.

The module supports both common formats like `mm/dd/yyyy` and
`dd/mm/yyyy`, with the ability to distinguish based on the
`month_first` parameter.

Note: If you think a new format should be supported, feel free to ask
for it, and I will try to add it in a future update.

## Error Handling

- If the input text is incomplete or not recognizable as a valid
  date/time, a `ValueError` may be raised.

- The module tries to handle incomplete dates (for instance, "october"
  is equivalent to "the first of october of this year"), but very
  ambiguous cases as "9" are just rejected.

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
  dates. Note that as of October 2024, it has not been updated for a
  long time.

- [`Arrow`](https://arrow.readthedocs.io/en/latest/): A `datetime`
  alternative with a focus on usability. The
  [`dehumanize`](https://arrow.readthedocs.io/en/latest/guide.html#dehumanize)
  feature allows one to parse time deltas expressed in natural
  language.

## License

Copyright (c) 2024 Salvador Fandiño García

This project is licensed under the MIT License. See the `LICENSE` file for more details.
