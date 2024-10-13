## Module: Date and Time Parsing

This Python module provides three key methods for parsing text into time, date, or datetime objects. These methods are:

### 1. `parse_time(text)`

- **Description**: Extracts time information from a given string and returns a time object. This function is suitable for parsing times like "2:45 PM", "14:30", "midnight", etc.

- **Parameters**:
  - `text` (str): The text containing time information to be parsed.

- **Returns**: A `datetime.time` object.

- **Example**:
  ```python
  time_obj = parse_time("2:45 PM")
  # Returns: datetime.time(14, 45)
  ```

### 2. `parse_date(text, now=None, month_first=True)`

- **Description**: Parses date information from a given string and returns a date object. The function can handle different formats including relative date descriptions (e.g., "next month", "last Friday") or explicit dates (e.g., "10/3/2017", "15th of July").

- **Parameters**:
  - `text` (str): The text containing date information to be parsed.
  - `now` (datetime.date or datetime.datetime, optional): The reference date to use for relative expressions. Defaults to the current date if not specified.
  - `month_first` (bool, optional): Indicates whether the month appears first in numerical dates (e.g., `10/3` is treated as October 3rd if `month_first=True`). Defaults to `True`.

- **Returns**: A `datetime.date` object.

- **Example**:
  ```python
  date_obj = parse_date("the first of next month")
  # Assuming today is 2023-10-10, returns: datetime.date(2023, 11, 1)
  ```

### 3. `parse_datetime(text, now=None, month_first=True)`

- **Description**: Parses both date and time information from a given string and returns a datetime object. The function handles a wide range of date and time formats, including explicit and relative formats.

- **Parameters**:
  - `text` (str): The text containing datetime information to be parsed.
  - `now` (datetime.date or datetime.datetime, optional): The reference date to use for relative expressions. Defaults to the current date and time if not specified.
  - `month_first` (bool, optional): Indicates whether the month appears first in numerical dates (e.g., `10/3` is treated as October 3rd if `month_first=True`). Defaults to `True`.

- **Returns**: A `datetime.datetime` object.

- **Example**:
  ```python
  datetime_obj = parse_datetime("january 1, 2017 at 14:30")
  # Returns: datetime.datetime(2017, 1, 1, 14, 30)
  ```

### Supported Formats

The module can parse a wide variety of date and time formats, including but not limited to:

- **Relative Dates**: "the first of next month", "next week", "last Friday", "the day after tomorrow".
- **Explicit Dates**: "10/3/2017", "march 15, 2017", "15/july/2023".
- **Relative Weekdays**: "monday next week", "last monday", "second sunday of 2023".
- **Datetime Formats**: "january 1, 2017 at 14:30", "february 14, 2017 at 2:45 PM".

The module supports both common formats like `mm/dd/yyyy` and `dd/mm/yyyy`, with the ability to distinguish based on the `month_first` parameter.

### Error Handling

- If the input text is incomplete or not recognizable as a valid date/time, a `ValueError` may be raised.
- For instance, providing just a day without a month or year (e.g., "15") will raise an error, as it's ambiguous.

### Example Usage

```python
from your_module_name import parse_date, parse_time, parse_datetime

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

### See Also

- `datetime` module: For working with date and time objects in Python.
- `time` module: Provides various time-related functions, such as working with timestamps or sleep functions. This can be useful in combination with date and time parsing.
- `dateutil.relativedelta`: For relative date calculations, like adding or subtracting months or years.
- `calendar` module: For calendar-related functions, such as determining leap years or getting the number of days in a month.
- `dateparser` library: A library similar to this module, which parses natural language dates. Note that `dateparser` is older but currently unmaintained.
- `pytz` library: For handling time zones in Python. It can be useful when parsing dates and times that involve different time zones or when converting between local times and UTC.

### License

Copyright (c) 2024 Your Name

This project is licensed under the MIT License. See the `LICENSE` file for more details.
