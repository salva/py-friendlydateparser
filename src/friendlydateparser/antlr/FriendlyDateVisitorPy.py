from .FriendlyDateVisitor import FriendlyDateVisitor
from .FriendlyDateParser import FriendlyDateParser
import functools
from datetime import datetime, time, date
import traceback
import sys
import logging

traceme = True

def trace(func):
    if traceme:
        @functools.wraps(func)
        def wrapper(self, ctx, *args, **kwargs):
            tree = ctx.toStringTree(recog=ctx.parser) if ctx else "None"
            logging.warning(f">>> method call {func.__name__}({tree})...")
            result = func(self, ctx, *args, **kwargs)
            logging.warning(f"<<<  method call {func.__name__}({tree}) ---> {result}")
            return result
        return wrapper
    else:
        return func

def _fix_time_parts(hour, minute, second, micros, am_pm):
    if hour is None:
        hour = 0
    if minute is None:
        minute = 0
    if second is None:
        second = 0
    if micros is None:
        micros = 0

    if am_pm is not None:
        if hour >= 12:
            if hour == 12:
                hour = 0
            else:
                raise ValueError("Invalid time: hour value out of range")
        if am_pm:
            hour += 12

    return hour, minute, second, micros

def _fix_date_parts(year, month, day, now):
    if year is None:
        year = now.year
        if month is None:
            month = now.month
            if day is None:
                day = now.day

    if month is None:
        month = 1
    if day is None:
        day = 1
    return year, month, day


def _check_time_parts(hour, minute, second, micros):
    if hour < 0 or hour > 23:
        raise ValueError("Invalid time: hour value out of range")
    if minute < 0 or minute > 59:
        raise ValueError("Invalid time: minute value out of range")
    if second < 0 or second > 59:
        raise ValueError("Invalid time: second value out of range")
    if micros < 0 or micros > 999999:
        raise ValueError("Invalid time: microsecond value out of range")

def _check_date_parts(year, month, day):
    if month < 1 or month > 12:
        raise ValueError("Invalid date: month value out of range")
    if day < 1 or day > 31:
        raise ValueError("Invalid date: day value out of range")

class FriendlyDateVisitorPy(FriendlyDateVisitor):
    def __init__(self, now, month_first, _trace_visiting=False):
        if not isinstance(now, datetime):
            raise ValueError(f"now must be a datetime object instead of one with type {type(now).__name__}")
        self._now = now
        self._month_first = month_first
        self._month_ix = 0 if month_first else 1
        self._day_ix = 1 if month_first else 0

    @trace
    def visit(self, ctx):
        return super().visit(ctx)

    @trace
    def visitChildren(self, ctx):
        return super().visitChildren(ctx)

    @trace
    def make_datetime(self, ctx:FriendlyDateParser.FriendlyDateContext):
        try:
            year, month, day, hour, minute, second, micros, am_pm = self.visit(ctx)
        except Exception as e:
            logging.exception(e)
            raise Exception(f"Error parsing date: {ctx.toStringTree(recog=ctx.parser)}") from e

        year, month, day = _fix_date_parts(year, month, day, self._now)
        hour, minute, second, micros = _fix_time_parts(hour, minute, second, micros, am_pm)

        _check_date_parts(year, month, day)
        _check_time_parts(hour, minute, second, micros)

        logging.warning(f"make_datetime: {year}-{month}-{day}T{hour}:{minute}:{second}.{micros}")
        return datetime(year, month, day, hour, minute, second, micros)

    @trace
    def make_date(self, ctx:FriendlyDateParser.FriendlyDateContext):
        try:
            year, month, day = self.visit(ctx)
        except Exception as e:
            logging.exception(e)
            raise Exception(f"Error parsing date: {ctx.toStringTree(recog=ctx.parser)}") from e

        year, month, day = _fix_date_parts(year, month, day, self._now)
        _check_date_parts(year, month, day)

        return date(year, month, day)

    @trace
    def make_time(self, ctx:FriendlyDateParser.FriendlyTimeContext):
        try:
            hour, minute, second, micros, am_pm = self.visit(ctx)
        except Exception as e:
            logging.exception(e)
            raise Exception(f"Error parsing time: {ctx.toStringTree(recog=ctx.parser)}") from e

        hour, minute, second, micros = _fix_time_parts(hour, minute, second, micros, am_pm)

        _check_time_parts(hour, minute, second, micros)

        return time(hour, minute, second, micros)

    @trace
    def visitFriendlyTime(self, ctx:FriendlyDateParser.FriendlyTimeContext):
        return self.visitTime(ctx.time())

    @trace
    def visitFriendlyDate(self, ctx:FriendlyDateParser.FriendlyDateContext):
        return self.visitDate(ctx.date())

    @trace
    def visitFriendlyDateTime(self, ctx:FriendlyDateParser.FriendlyDateTimeContext):
        return self.visitDateTime(ctx.dateTime())

    @trace
    def visitDateTime(self, ctx:FriendlyDateParser.DateTimeContext):
        logging.error("visitDateTime")
        if (c := ctx.date()):
            year, month, day = self.visitDate(ctx.date())
        else:
            year, month, day = None, None, None

        if (c := ctx.time()):
            print("time!")
            hour, minute, second, micros, am_pm = self.visitTime(ctx.time())
        else:
            hour, minute, second, micros, am_pm = None, None, None, None, None

        return (year, month, day, hour, minute, second, micros, am_pm)

    @trace
    def visitTime(self, ctx:FriendlyDateParser.TimeContext):
        if (c := ctx.timeAbsolute()):
            return self.visitTimeAbsolute(c)
        elif ctx.MIDNIGHT():
            return (0, 0, 0, 0, None)
        elif ctx.NOON() or ctx.MIDDAY():
            return (12, 0, 0, 0, None)
        else:
            raise ValueError("Internal error, unexpected branch")

    @trace
    def visitTimeAbsolute(self, ctx:FriendlyDateParser.TimeAbsoluteContext):
        hour = self.visitHour(ctx.hour())
        minute = self.visitMinute(c) if (c := ctx.minute()) else None
        if (c := ctx.second()):
            second, micros = self.visitSecond(c)
        else:
            second, micros = None, None
        am_pm = self.visitAmPm(c) if (c := ctx.amPm()) else None
        return (hour, minute, second, micros, am_pm)

    @trace
    def visitHour(self, ctx:FriendlyDateParser.HourContext):
        return int(ctx.TWO_DIGIT_NUMBER().getText())

    @trace
    def visitMinute(self, ctx:FriendlyDateParser.MinuteContext):
        return int(ctx.TWO_DIGIT_NUMBER().getText())

    @trace
    def visitSecond(self, ctx:FriendlyDateParser.SecondContext):
        if (c := ctx.TWO_DIGIT_NUMBER()):
            return (int(c.getText()), 0)
        if (c := ctx.SECONDS_FLOAT_NUMBER()):
            a, b = c.getText().split('.')
            b += '000000'
            return (int(a), int(b[:6]))
        else:
            raise ValueError("Internal error parsing seconds")

    @trace
    def visitAmPm(self, ctx:FriendlyDateParser.AmPmContext):
        return ctx.PM() is not None

    @trace
    def visitDateMonthAsName(self, ctx:FriendlyDateParser.DateMonthAsNameContext):
        if (c := ctx.dayAsNumber()):
            day = self.visitDayAsNumber(c)
        elif (c := ctx.dayAsOrdinal()):
            day = self.visitDayAsOrdinal(c)
        elif (c := ctx.dayAsNumberOrOrdinal()):
            day = self.visitDayAsNumberOrOrdinal(c)
        else:
            day = None

        month = self.visitMonthAsName(ctx.monthAsName())

        if (c := ctx.yearLong()):
            year = self.visitYearLong(c)
        else:
            year = None

        return (year, month, day)

    @trace
    def visitDateMonthAsNumber(self, ctx:FriendlyDateParser.DateMonthAsNumberContext):
        if (c := ctx.monthAsNumber()):
            month = self.visitMonthAsNumber(c)
            if (c := ctx.dayAsNumber()):
                day = self.visitDayAsNumber(c)
            else:
                day = None
        else:
            month = self.visitTwoDigitNumber(ctx.twoDigitNumber(self._month_ix))
            day = self.visitTwoDigitNumber(ctx.twoDigitNumber(self._day_ix))

        if (c := ctx.yearLong()):
            year = self.visitYearLong(c)
        else:
            year = None

        return (year, month, day)

    @trace
    def visitDateYearAlone(self, ctx:FriendlyDateParser.DateYearAloneContext):
        year = self.visitYearLong(ctx.yearLong())
        return (year, None, None)

    @trace
    def visitMonthAsName(self, ctx:FriendlyDateParser.MonthAsNameContext):
        return ctx.value

    @trace
    def visitDayAsOrdinal(self, ctx:FriendlyDateParser.DayAsOrdinalContext):
        return int(ctx.DAY_AS_ORDINAL().getText()[:-2])

    @trace
    def visitTwoDigitNumber(self, ctx:FriendlyDateParser.TwoDigitNumberContext):
        return int(ctx.TWO_DIGIT_NUMBER().getText())

    @trace
    def visitDayAsNumber(self, ctx:FriendlyDateParser.DayAsNumberContext):
        return super().visitDayAsNumber(ctx)

    @trace
    def visitFourDigitNumber(self, ctx:FriendlyDateParser.FourDigitNumberContext):
        return int(ctx.FOUR_DIGIT_NUMBER().getText())

    @trace
    def visitDateRelative(self, ctx:FriendlyDateParser.DateRelativeContext):
        return (None, None, None) # TODO

