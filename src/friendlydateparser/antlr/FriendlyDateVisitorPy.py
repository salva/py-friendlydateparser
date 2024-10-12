from .FriendlyDateVisitor import FriendlyDateVisitor
from .FriendlyDateParser import FriendlyDateParser
import functools
from datetime import datetime, time, date, timedelta
from dateutil.relativedelta import relativedelta
from calendar import monthrange
import logging
import os

traceme = True or os.environ.get("FRIENDLYDATEPARSER_TRACE", "0") == "1"

ordinal_word2number = { 'first': 1, 'second': 2, 'third': 3, 'fourth': 4, 'fifth': 5,
                        'sixth': 6, 'seventh': 7, 'eighth': 8, 'ninth': 9, 'tenth': 10,
                        'eleventh': 11, 'twelfth': 12, 'thirteenth': 13, 'fourteenth': 14,
                        'fifteenth': 15, 'sixteenth': 16, 'seventeenth': 17,
                        'eighteenth': 18, 'nineteenth': 19, 'twentieth': 20,
                        'twenty-first': 21, 'twenty-second': 22, 'twenty-third': 23,
                        'twenty-fourth': 24, 'twenty-fifth': 25, 'twenty-sixth': 26,
                        'twenty-seventh': 27, 'twenty-eighth': 28, 'twenty-ninth': 29,
                        'thirtieth': 30, 'thirty-first': 31 }

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

    # @trace
    # def visitChildren(self, ctx):
    #    return super().visitChildren(ctx)

    @trace
    def visit(self, ctx):
        try:
            return super().visit(ctx)
        except Exception as e:
            logging.exception(e)
            raise ValueError(f"Error parsing {ctx.toStringTree(recog=ctx.parser)}") from e


    @trace
    def visitFriendlyTime(self, ctx:FriendlyDateParser.FriendlyTimeContext):
        return self.visitChildren(ctx)['time']

    @trace
    def visitFriendlyDate(self, ctx:FriendlyDateParser.FriendlyDateContext):
        return self.visitChildren(ctx)['date']

    @trace
    def visitFriendlyDateTime(self, ctx:FriendlyDateParser.FriendlyDateTimeContext):
        return self.visitChildren(ctx)['datetime']

    @trace
    def visitTime(self, ctx:FriendlyDateParser.FriendlyTimeContext):
        return {'time': self._make_time(self.visitChildren(ctx))}

    @trace
    def visitDateRelativeByDate(self, ctx:FriendlyDateParser.FriendlyDateContext):
        return {'date': self._make_date_relative(self.visitChildren(ctx))}

    @trace
    def visitDateAbsolute(self, ctx:FriendlyDateParser.DateAbsoluteContext):
        return {'date': self._make_date_absolute(self.visitChildren(ctx))}

    @trace
    def visitDateTime(self, ctx:FriendlyDateParser.FriendlyDateTimeContext):
        return {'datetime': self._make_datetime(self.visitChildren(ctx))}

    @trace
    def visitLastDay(self, ctx:FriendlyDateParser.LastDayContext):
        return {'day': -1 }

    @trace
    def visitLastWeek(self, ctx:FriendlyDateParser.LastWeekContext):
        return {'week': -1 }

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
    def visitWeekNumber(self, ctx:FriendlyDateParser.WeekNumberContext):
        return self._promote_tdn(ctx, 'week')

    @trace
    def visitDayAsOrdinal(self, ctx:FriendlyDateParser.DayAsOrdinalContext):
        return {'day': self.visitChildren(ctx)}

    @trace
    def visitTwoDigitOrdinal(self, ctx:FriendlyDateParser.TwoDigitOrdinalContext):
        return int(ctx.TWO_DIGIT_ORDINAL().getText()[:-2])

    @trace
    def visitWordOrdinal(self, ctx:FriendlyDateParser.WordOrdinalContext):
        return ordinal_word2number[ctx.WORD_ORDINAL().getText()]

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
    def visitToday(self, ctx:FriendlyDateParser.TodayContext):
        return {'rule': today, 'delta': 0}

    @trace
    def visitTomorrow(self, ctx:FriendlyDateParser.TomorrowContext):
        return {'rule': 'today', 'delta': 1}

    @trace
    def visitYesterday(self, ctx:FriendlyDateParser.YesterdayContext):
        return {'rule': 'today', 'delta': -1}

    @trace
    def visitTheDayAfterTomorrow(self, ctx:FriendlyDateParser.TheDayAfterTomorrowContext):
        return {'rule': 'today', 'delta': 2}

    @trace
    def visitTheDayBeforeYesterday(self, ctx:FriendlyDateParser.TheDayBeforeYesterdayContext):
        return {'rule': 'today', 'delta': -2}

    @trace
    def visitDateRelativeDay(self, ctx:FriendlyDateParser.DateRelativeDayContext):
        r = self.visitChildren(ctx)
        r['rule'] = 'day'
        return r

    @trace
    def visitDateRelativeWeek(self, ctx:FriendlyDateParser.DateRelativeWeekContext):
        r = self.visitChildren(ctx)
        r['rule'] = 'week'
        return r

    @trace
    def visitDateRelativeMonth(self, ctx:FriendlyDateParser.DateRelativeMonthContext):
        r = self.visitChildren(ctx)
        r['rule'] = 'month'
        return r

    @trace
    def visitDateRelativeYearWithMonth(self, ctx:FriendlyDateParser.DateRelativeYearWithMonthContext):
        r = self.visitChildren(ctx)
        r['rule'] = 'year'
        return r

    @trace
    def visitDateRelativeYearWithoutMonth(self, ctx:FriendlyDateParser.DateRelativeYearWithoutMonthContext):
        r = self.visitChildren(ctx)
        r['rule'] = 'year'
        return r

    @trace
    def visitWeekDay(self, ctx:FriendlyDateParser.WeekDayContext):
        return {'weekday': ctx.value}

    @trace
    def visitLast(self, ctx:FriendlyDateParser.LastContext):
        return {'modifier': 'last'}

    @trace
    def visitNext_(self, ctx:FriendlyDateParser.Next_Context):
        return {'modifier': 'next'}

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

    def _make_date_absolute(self, r):
        if r.get('week') is not None:
            return self._make_date_absolute_by_week(r)

        year = r.get('year')
        month = r.get('month')
        day = r.get('day')
        week = r.get('week')

        if year is None:
            year = self._now.year
            if month is None:
                month = self._now.month
                if day is None:
                    day = self._now.day

        if month is None:
            month = 12 if day == -1 else 1
        elif month == 0 or month > 12:
            raise ValueError("Invalid date: month value out of range")

        last_day = monthrange(year, month)[1]
        if day is None:
            day = 1
        elif day == -1:
            day = last_day
        elif day == 0 or day > last_day:
            raise ValueError("Invalid date: day value out of range")

        return date(year, month, day)

    def _make_date_absolute_by_week(self, r):
        week = r['week']
        if week == 0:
            raise ValueError("Invalid date: week value out of range")
        year = r.get('year', self._now.year)
        month = r.get('month')
        if month is not None and (month == 0 or month > 12):
            raise ValueError("Invalid date: month value out of range")
        weekday = r.get('weekday', 0)

        if week == -1:
            week = 0
            if month is None:
                year += 1
            elif month < 12:
                month += 1
            elif month == 12:
                month = 1
                year += 1

        first_day = date(year, month or 1, 1)
        first_weekday = first_day.weekday()
        if first_weekday <= 3:
            week -= 1

        monday = first_day + timedelta(days=7*week-first_weekday)
        wednesday = monday + timedelta(days=3)

        if wednesday.year > year or \
           (month is not None and wednesday.year == year and wednesday.month > month):
            raise ValueError("Invalid date: week value out of range")

        return monday + timedelta(days=weekday)

    def _make_datetime(self, r):
        date = r['date']
        time = r.get('time', datetime.min.time())
        return datetime.combine(date, time)


    def _make_date_relative(self, r):
        now = r.get('date', self._now.date())
        rule = r['rule']
        if rule == 'today':
            return self._make_date_relative_day_delta(r, now, r['delta'])
        if rule == 'day':
            return self._make_date_relative_day(r, now)
        if rule == 'week':
            return self._make_date_relative_week(r, now)
        if rule == 'month':
            return self._make_date_relative_month(r, now)
        if rule == 'year':
            return self._make_date_relative_year(r, now)

    def _make_date_relative_day_delta(self, r, now, delta):
        return now + relativedelta(days=delta)

    def _make_date_relative_day(self, r, now):
        weekday = r['weekday']
        today = now.weekday()
        modifier = r.get('modifier')
        delta = weekday - today
        if modifier == 'next':
            if delta < 1:
                delta += 7
            return now + relativedelta(days=delta)
        if modifier == 'last':
            if delta > 0:
                delta -= 7
            return now + relativedelta(days=delta)
        return self._this_weekday(now, weekday)

    def _make_date_relative_week(self, r, now):
        date = self._this_weekday(now, r.get('weekday', 0))
        if r['modifier'] == 'last':
            return date - relativedelta(days=7)
        if r['modifier'] == 'next':
            return date + relativedelta(days=7)
        return date

        today = now.weekday()
        delta = weekday - today
        if delta < 1:
            delta += 7
        return now + relativedelta(days=delta)

    def _make_date_relative_month(self, r, now):
        year = r.get('year', now.year)
        month = r.get('month')

        if month is None:
            d = date(year, now.month, 1)
            if r['modifier'] == 'last':
                d = d - relativedelta(months=1)
            elif r['modifier'] == 'next':
                d = d + relativedelta(months=1)

            year = d.year
            month = d.month
        else:
            if r['modifier'] == 'last':
                if month >= now.month:
                    year -= 1
            elif r['modifier'] == 'next':
                if month <= now.month:
                    year += 1

        last_day = monthrange(year, month)[1]
        day = r.get('day', 1)
        if day == -1:
            day = last_day
        elif day > last_day:
            raise ValueError("Invalid date: day value out of range")

        return date(year, month, day)

    def _make_date_relative_year(self, r, now):
        year = r.get('year', now.year)
        if r['modifier'] == 'last':
            year -= 1
        elif r['modifier'] == 'next':
            year += 1
        day = r.get('day', 1)
        month = r.get('month', 12 if day == -1 else 1)

        last_day = monthrange(year, month)[1]
        if day == -1:
            day = last_day

        return date(year, month, day)

    def _this_monday(self, date):
        return date - relativedelta(days=date.weekday())

    def _this_weekday(self, date, weekday):
        return date - relativedelta(days=date.weekday() - weekday)
