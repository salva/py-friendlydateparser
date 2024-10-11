from .FriendlyDateVisitor import FriendlyDateVisitor
from .FriendlyDateParser import FriendlyDateParser
import functools
from datetime import datetime, time, date
from calendar import monthrange
import logging
import os

traceme = True or os.environ.get("FRIENDLYDATEPARSER_TRACE", "0") == "1"

def trace(func):
    if traceme:
        @functools.wraps(func)
        def wrapper(self, ctx, *args, **kwargs):
            tree = ctx.toStringTree(recog=ctx.parser) if ctx else "None"
            logging.debug(f">>> method call {func.__name__}({tree})...")
            result = func(self, ctx, *args, **kwargs)
            logging.debug(f"<<<  method call {func.__name__}({tree}) ---> {result}")
            return result
        return wrapper
    else:
        return func


class FriendlyDateVisitorPy(FriendlyDateVisitor):
    def __init__(self, now, month_first):
        if not isinstance(now, datetime):
            raise ValueError(f"now must be a datetime object instead of one with type {type(now).__name__}")
        self._now = now
        self._month_first = month_first
        self._left_slot = 'month' if month_first else 'day'
        self._right_slot = 'day' if month_first else 'month'

    def aggregateResult(self, aggregate, nextResult):
        if nextResult is None:
            return aggregate
        if isinstance(aggregate, dict) and isinstance(nextResult, dict):
            return {**aggregate, **nextResult} # shallow merge!
        return nextResult

    #@trace
    def visitChildren(self, ctx):
        return super().visitChildren(ctx)

    @trace
    def visit(self, ctx):
        try:
            return super().visit(ctx)
        except Exception as e:
            logging.exception(e)
            raise ValueError(f"Error parsing {ctx.toStringTree(recog=ctx.parser)}") from e

    @trace
    def visitFriendlyTime(self, ctx:FriendlyDateParser.FriendlyTimeContext):
        return self._make_time(self.visitChildren(ctx))

    @trace
    def visitFriendlyDate(self, ctx:FriendlyDateParser.FriendlyDateContext):
        return self._make_date(self.visitChildren(ctx))

    @trace
    def visitFriendlyDateTime(self, ctx:FriendlyDateParser.FriendlyDateTimeContext):
        return self._make_datetime(self.visitChildren(ctx))

    @trace
    def visitAtTime(self, ctx:FriendlyDateParser.AtTimeContext):
        return {'at_time': self.visitChildren(ctx)}

    @trace
    def visitMidnight(self, ctx:FriendlyDateParser.MidnightContext):
        return {'hour': 0, 'minute': 0, 'second': 0, 'microsecond': 0}

    @trace
    def visitNoon(self, ctx:FriendlyDateParser.NoonContext):
        return {'hour': 12, 'minute': 0, 'second': 0, 'microsecond': 0}

    @trace
    def visitHour(self, ctx:FriendlyDateParser.HourContext):
        return self._promote_tdn(ctx, 'hour')

    @trace
    def visitMinute(self, ctx:FriendlyDateParser.MinuteContext):
        return self._promote_tdn(ctx, 'minute')

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
    def visitAm(self, ctx:FriendlyDateParser.AmContext):
        return {'am': True}

    @trace
    def visitPm(self, ctx:FriendlyDateParser.PmContext):
        return {'pm': True}

    @trace
    def visitTwoDigitNumberLeft(self, ctx:FriendlyDateParser.TwoDigitNumberLeftContext):
        return self._promote_tdn(ctx, self._left_slot)

    @trace
    def visitTwoDigitNumberRight(self, ctx:FriendlyDateParser.TwoDigitNumberRightContext):
        return self._promote_tdn(ctx, self._right_slot)

    @trace
    def visitSecond(self, ctx:FriendlyDateParser.SecondContext):
        (a, b) = self.visitTwoDigitFloatNumber(ctx.twoDigitFloatNumber())
        return {'second': a, 'microsecond': b}

    @trace
    def visitYearLong(self, ctx:FriendlyDateParser.YearLongContext):
        return {'year': self.visitFourDigitNumber(ctx.fourDigitNumber())}

    @trace
    def visitMonthAsName(self, ctx:FriendlyDateParser.MonthAsNameContext):
        return {'month': ctx.value}

    @trace
    def visitMonthAsNumber(self, ctx:FriendlyDateParser.MonthAsNumberContext):
        return self._promote_tdn(ctx, 'month')

    @trace
    def visitDayAsOrdinal(self, ctx:FriendlyDateParser.DayAsOrdinalContext):
        return {'day': int(ctx.DAY_AS_ORDINAL().getText()[:-2])}

    @trace
    def visitDayAsNumber(self, ctx:FriendlyDateParser.DayAsNumberContext):
        return self._promote_tdn(ctx, 'day')

    @trace
    def visitTwoDigitNumber(self, ctx:FriendlyDateParser.TwoDigitNumberContext):
        return int(ctx.TWO_DIGIT_NUMBER().getText())

    @trace
    def visitFourDigitNumber(self, ctx:FriendlyDateParser.FourDigitNumberContext):
        return int(ctx.FOUR_DIGIT_NUMBER().getText())

    @trace
    def visitTwoDigitFloatNumber(self, ctx:FriendlyDateParser.TwoDigitFloatNumberContext):
        if (c := ctx.TWO_DIGIT_NUMBER()):
            return (int(c.getText()), 0)
        (a, b) = ctx.TWO_DIGIT_FLOAT_NUMBER().getText().split('.')
        b += "000000"
        return (int(a), int(b[:6]))

    @trace
    def visitDateRelative(self, ctx:FriendlyDateParser.DateRelativeContext):
        return {} # TODO


    def _promote_tdn(self, ctx, slot):
        return {slot: self.visitTwoDigitNumber(ctx.twoDigitNumber())}

    def _make_time(self, r):
        hour = r.get('hour', 0)
        minute = r.get('minute', 0)
        second = r.get('second', 0)
        microsecond = r.get('microsecond', 0)
        am = r.get('am', False)
        pm = r.get('pm', False)

        if pm or am:
            if hour >= 12:
                if hour == 12:
                    hour = 0
                else:
                    raise ValueError("Invalid time: hour value out of range")
            if pm:
                hour += 12
        elif hour > 23:
            raise ValueError("Invalid time: hour value out of range")
        if minute > 59:
            raise ValueError("Invalid time: minute value out of range")
        if second > 59:
            raise ValueError("Invalid time: second value out of range")

        return time(hour, minute, second, microsecond)

    def _make_date(self, r):

        year = r.get('year')
        month = r.get('month')
        day = r.get('day')

        if year is None:
            year = self._now.year
            if month is None:
                month = self._now.month
                if day is None:
                    day = self._now.day
        if month is None:
            month = 1
        if day is None:
            day = 1

        if month > 12:
            raise ValueError("Invalid date: month value out of range")
        if day > monthrange(year, month)[1]:
            raise ValueError("Invalid date: day value out of range")

        return date(year, month, day)

    def _make_datetime(self, r):
        date = self._make_date(r)
        time = self._make_time(r.get('at_time', {}))
        return datetime.combine(date, time)
