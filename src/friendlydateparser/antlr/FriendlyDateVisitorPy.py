from .FriendlyDateVisitor import FriendlyDateVisitor
from .FriendlyDateParser import FriendlyDateParser
import functools
from datetime import datetime, time, date, timedelta
from dateutil.relativedelta import relativedelta
import pytz
from calendar import monthrange
import logging
import os

from friendlydateparser.tz_abbreviations import tz_abbreviations

traceme = os.environ.get("FRIENDLYDATEPARSER_TRACE", "0") == "1"

ordinals = [ 'first', 'second', 'third', 'fourth', 'fifth', 'sixth',
             'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth',
             'thirteenth', 'fourteenth', 'fifteenth', 'sixteenth',
             'seventeenth', 'eighteenth', 'nineteenth', 'twentieth',
             'twenty-first', 'twenty-second', 'twenty-third', 'twenty-fourth',
             'twenty-fifth', 'twenty-sixth', 'twenty-seventh', 'twenty-eighth',
             'twenty-ninth', 'thirtieth', 'thirty-first', 'thirty-second',
             'thirty-third', 'thirty-fourth', 'thirty-fifth', 'thirty-sixth',
             'thirty-seventh', 'thirty-eighth', 'thirty-ninth', 'fortieth',
             'forty-first', 'forty-second', 'forty-third', 'forty-fourth',
             'forty-fifth', 'forty-sixth', 'forty-seventh', 'forty-eighth',
             'forty-ninth', 'fiftieth', 'fifty-first', 'fifty-second',
             'fifty-third', 'fifty-fourth', 'fifty-fifth', 'fifty-sixth',
             'fifty-seventh', 'fifty-eighth', 'fifty-ninth', 'sixtieth',
             'sixty-first', 'sixty-second', 'sixty-third', 'sixty-fourth',
             'sixty-fifth', 'sixty-sixth', 'sixty-seventh', 'sixty-eighth',
             'sixty-ninth', 'seventieth', 'seventy-first', 'seventy-second',
             'seventy-third', 'seventy-fourth', 'seventy-fifth',
             'seventy-sixth', 'seventy-seventh', 'seventy-eighth',
             'seventy-ninth', 'eightieth', 'eighty-first', 'eighty-second',
             'eighty-third', 'eighty-fourth', 'eighty-fifth', 'eighty-sixth',
             'eighty-seventh', 'eighty-eighth', 'eighty-ninth', 'ninetieth',
             'ninety-first', 'ninety-second', 'ninety-third', 'ninety-fourth',
             'ninety-fifth', 'ninety-sixth', 'ninety-seventh', 'ninety-eighth',
             'ninety-ninth' ]
ordinal2number = {ordinal: index + 1 for index, ordinal in enumerate(ordinals)}

weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def tz_abbreviation2pytz(abv):
    offset = tz_abbreviations[abv.upper()]
    return pytz.FixedOffset(offset)

def trace(func):
    if traceme:
        @functools.wraps(func)
        def wrapper(self, ctx, *args, **kwargs):
            tree = ctx.toStringTree(recog=ctx.parser) if ctx else "None"
            logging.debug(f">>> method call {func.__name__}({tree})...")
            try:
                result = func(self, ctx, *args, **kwargs)
                logging.debug(f"<<<  method call {func.__name__}({tree}) ---> {result}")
                return result
            except Exception as e:
                logging.exception(f"<<<  method call {func.__name__}({tree}) EXCEPTION!")
                raise
        return wrapper
    else:
        return func

class FriendlyDateVisitorPy(FriendlyDateVisitor):
    def __init__(self, now, month_first, default_tz):
        if not isinstance(now, datetime):
            raise ValueError(f"now must be a datetime object instead of one with type {type(now).__name__}")
        self._now = now
        self._month_first = month_first
        self._default_tz = default_tz
        self._left_slot = 'month' if month_first else 'day'
        self._right_slot = 'day' if month_first else 'month'

    def aggregateResult(self, aggregate, nextResult):
        if nextResult is None:
            return aggregate
        if isinstance(aggregate, dict) and isinstance(nextResult, dict):
            return {**aggregate, **nextResult} # shallow merge!
        if isinstance(aggregate, list) and isinstance(nextResult, list):
            return aggregate + nextResult
        return nextResult

    # @trace
    # def visitChildren(self, ctx):
    #    return super().visitChildren(ctx)

    @trace
    def visit(self, ctx):
        return super().visit(ctx)

    @trace
    def visitFriendlyDate(self, ctx:FriendlyDateParser.FriendlyDateContext):
        return self.visitChildren(ctx)['date']

    @trace
    def visitFriendlyDateTime(self, ctx:FriendlyDateParser.FriendlyDateTimeContext):
        return self.visitChildren(ctx)['datetime']

    @trace
    def visitFriendlyTimezone(self, ctx:FriendlyDateParser.FriendlyTimezoneContext):
        return self.visitChildren(ctx)['tz']

    @trace
    def visitNow(self, ctx:FriendlyDateParser.NowContext):
        return {'datetime': self._now}

    @trace
    def visitTime(self, ctx:FriendlyDateParser.TimeContext):
        return {'time': self._make_time(self.visitChildren(ctx))}

    @trace
    def visitIso8601Time(self, ctx:FriendlyDateParser.Iso8601TimeContext):
        return {'time': self._make_time(self.visitChildren(ctx))}

    @trace
    def visitIso8601Month(self, ctx:FriendlyDateParser.Iso8601MonthContext):
        return {'month': self.visitNumber2(ctx.number2())}

    @trace
    def visitIso8601YearWeek(self, ctx:FriendlyDateParser.Iso8601YearWeekContext):
        return { 'week': self.visitNumber2(ctx.number2()) }

    @trace
    def visitIso8601WeekDay(self, ctx:FriendlyDateParser.Iso8601WeekDayContext):
        return { 'weekday': self.visitNumber1(ctx.number1()) - 1 }

    @trace
    def visitIso8601YearDay(self, ctx:FriendlyDateParser.Iso8601YearDayContext):
        return { 'day_position': self.visitNumber3(ctx.number3()) }

    @trace
    def visitIso8601MonthDay(self, ctx:FriendlyDateParser.Iso8601MonthDayContext):
        return { 'day': self.visitNumber2(ctx.number2()) }

    @trace
    def visitDateRelativeByDate(self, ctx:FriendlyDateParser.DateRelativeByDateContext):
        return {'date': self._make_date_relative(self.visitChildren(ctx))}

    @trace
    def visitDateAbsolute(self, ctx:FriendlyDateParser.DateAbsoluteContext):
        return {'date': self._make_date_absolute(self.visitChildren(ctx))}

    @trace
    def visitDateAlone(self, ctx:FriendlyDateParser.DateAloneContext):
        return {'date': self._make_date_alone(self.visitChildren(ctx))}


    @trace
    def visitIso8601Date(self, ctx:FriendlyDateParser.Iso8601DateContext):
        return {'date': self._make_date_absolute(self.visitChildren(ctx))}

    @trace
    def visitDateTime(self, ctx:FriendlyDateParser.FriendlyDateTimeContext):
        return {'datetime': self._make_datetime(self.visitChildren(ctx))}

    @trace
    def visitTz(self, ctx:FriendlyDateParser.TzContext):
        return {'tz': pytz.timezone(ctx.getText())}

    @trace
    def visitTzAbbreviation(self, ctx:FriendlyDateParser.TzAbbreviationContext):
        return {'tz': tz_abbreviation2pytz(ctx.getText())}

    @trace
    def visitTzOffset(self, ctx:FriendlyDateParser.TzOffsetContext):
        r = self.visitChildren(ctx)
        offset = r['hour']*60 + r.get('minute', 0)
        if ctx.DASH():
            offset = -offset
        return {'tz': pytz.FixedOffset(offset)}

    @trace
    def visitTzZ(self, ctx:FriendlyDateParser.TzZContext):
        return {'tz': pytz.UTC}

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
    def visitHour2(self, ctx:FriendlyDateParser.Hour2Context):
        return {'hour': self.visitNumber2(ctx.number2())}

    @trace
    def visitHour12(self, ctx:FriendlyDateParser.Hour12Context):
        return {'hour': self.visitNumber12(ctx.number12())}

    @trace
    def visitMinute2(self, ctx:FriendlyDateParser.Minute2Context):
        return {'minute': self.visitNumber2(ctx.number2())}

    @trace
    def visitMinute12(self, ctx:FriendlyDateParser.Minute12Context):
        return {'minute': self.visitNumber12(ctx.number12())}

    @trace
    def visitSecond2(self, ctx:FriendlyDateParser.Second2Context):
        a, b = self.visitFloat2(ctx.float2())
        return {'second': a, 'microsecond': b}

    @trace
    def visitSecond12(self, ctx:FriendlyDateParser.Second12Context):
        a, b = self.visitFloat12(ctx.float12())
        return {'second': a, 'microsecond': b}

    @trace
    def visitDateTimeDelta(self, ctx:FriendlyDateParser.DateTimeDeltaContext):
        return {'datetime_delta': self._make_datetime_delta(self.visitChildren(ctx))}

    @trace
    def visitDateDelta(self, ctx:FriendlyDateParser.DateDeltaContext):
        return {'date_delta': self._make_datetime_delta(self.visitChildren(ctx))}

    @trace
    def visitYearsDelta(self, ctx:FriendlyDateParser.YearsDeltaContext):
        return [{'years': self.visitZNumber(ctx.zNumber())}]

    @trace
    def visitMonthsDelta(self, ctx:FriendlyDateParser.MonthsDeltaContext):
        return [{'months': self.visitZNumber(ctx.zNumber())}]

    @trace
    def visitWeeksDelta(self, ctx:FriendlyDateParser.WeeksDeltaContext):
        return [{'weeks': self.visitZNumber(ctx.zNumber())}]

    @trace
    def visitDaysDelta(self, ctx:FriendlyDateParser.DaysDeltaContext):
        return [{'days': self.visitZNumber(ctx.zNumber())}]

    @trace
    def visitHoursDelta(self, ctx:FriendlyDateParser.HoursDeltaContext):
        return [{'hours': self.visitZNumber(ctx.zNumber())}]

    @trace
    def visitMinutesDelta(self, ctx:FriendlyDateParser.MinutesDeltaContext):
        return [{'minutes': self.visitZNumber(ctx.zNumber())}]

    @trace
    def visitSecondsDelta(self, ctx:FriendlyDateParser.SecondsDeltaContext):
        a, b = self.visitQNumber(ctx.qNumber())
        return [{'seconds': a, 'microseconds': b}]

    @trace
    def visitAm(self, ctx:FriendlyDateParser.AmContext):
        return {'am': True}

    @trace
    def visitPm(self, ctx:FriendlyDateParser.PmContext):
        return {'pm': True}

    @trace
    def visitNumber12Left(self, ctx:FriendlyDateParser.Number12LeftContext):
        return {self._left_slot: self.visitNumber12(ctx.number12())}

    @trace
    def visitNumber12Right(self, ctx:FriendlyDateParser.Number12RightContext):
        return {self._right_slot: self.visitNumber12(ctx.number12())}

    @trace
    def visitYear4(self, ctx:FriendlyDateParser.Year4Context):
        return {'year': self.visitNumber4(ctx.number4())}

    @trace
    def visitMonthAsName(self, ctx:FriendlyDateParser.MonthAsNameContext):
        return {'month': ctx.value}

    @trace
    def visitMonthAsNumber(self, ctx:FriendlyDateParser.MonthAsNumberContext):
        return {'month': self.visitNumber12(ctx.number12())}

    @trace
    def visitWeekNumber(self, ctx:FriendlyDateParser.WeekNumberContext):
        return {'week': self.visitNumber12(ctx.number12())}

    @trace
    def visitWeekDay(self, ctx:FriendlyDateParser.WeekDayContext):
        return { 'weekday': self.visitOneDigitNumber(ctx.oneDigitNumber()) }

    @trace
    def visitDayAsOrdinal(self, ctx:FriendlyDateParser.DayAsOrdinalContext):
        return {'day': self.visitChildren(ctx)}

    @trace
    def visitDayPositionOrdinal(self, ctx:FriendlyDateParser.DayPositionOrdinalContext):
        return {'day_position': self.visitChildren(ctx)}

    @trace
    def visitDayPositionNumber(self, ctx:FriendlyDateParser.DayPositionNumberContext):
        return {'day_position': self.visitChildren(ctx)}

    @trace
    def visitWeekDayPositionLast(self, ctx:FriendlyDateParser.WeekDayPositionLastContext):
        r = self.visitChildren(ctx)
        r['day_position'] = -1
        return r

    @trace
    def visitOrdinalDigits(self, ctx:FriendlyDateParser.OrdinalDigitsContext):
        return int(ctx.ORDINAL_DIGITS().getText()[:-2])

    @trace
    def visitWordOrdinal(self, ctx:FriendlyDateParser.WordOrdinalContext):
        if ctx.SECOND():
            return 2
        return ordinal2number[ctx.ORDINAL_WORDS().getText()]

    @trace
    def visitDayAsNumber(self, ctx:FriendlyDateParser.DayAsNumberContext):
        return {'day': self.visitNumber12(ctx.number12())}

    @trace
    def visitZNumber(self, ctx:FriendlyDateParser.ZNumberContext):
        v = self.visitNumber(ctx.number())
        return -v if ctx.DASH() else v

    @trace
    def visitNumber1(self, ctx:FriendlyDateParser.Number1Context):
        return int(ctx.ONE_DIGIT_NUMBER().getText())

    @trace
    def visitNumber2(self, ctx:FriendlyDateParser.Number2Context):
        return int(ctx.TWO_DIGIT_NUMBER().getText())

    @trace
    def visitNumber3(self, ctx:FriendlyDateParser.Number3Context):
        return int(ctx.THREE_DIGIT_NUMBER().getText())

    @trace
    def visitNumber4(self, ctx:FriendlyDateParser.Number4Context):
        return int(ctx.FOUR_DIGIT_NUMBER().getText())

    @trace
    def visitNumber(self, ctx:FriendlyDateParser.NumberContext):
        return int(ctx.getText())

    @trace
    def visitQNumber(self, ctx:FriendlyDateParser.QNumberContext):
        a, b = self.visitFloat(ctx.float_())
        if ctx.DASH():
            return (-a, -b)
        return (a, b)

    def _split_float(self, txt):
        a, *more = txt.split('.')
        b = more[0] if more else "0"
        b += "000000"
        return int(a), int(b[:6])

    @trace
    def visitFloat2(self, ctx:FriendlyDateParser.Float2Context):
        return self._split_float(ctx.getText())

    @trace
    def visitFloat12(self, ctx:FriendlyDateParser.Float12Context):
        return self._split_float(ctx.getText())

    @trace
    def visitFloat(self, ctx:FriendlyDateParser.FloatContext):
        return self._split_float(ctx.getText())

    @trace
    def visitBefore(self, ctx:FriendlyDateParser.BeforeContext):
        return {'delta_before': True}

    @trace
    def visitAgo(self, ctx:FriendlyDateParser.AgoContext):
        return {'delta_before': True}

    @trace
    def visitToday(self, ctx:FriendlyDateParser.TodayContext):
        return {'rule': 'today', 'delta': 0}

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
    def visitDateRelativeMonthWeek(self, ctx:FriendlyDateParser.DateRelativeMonthWeekContext):
        r = self.visitChildren(ctx)
        r['rule'] = 'month_week'
        return r

    @trace
    def visitDateRelativeYearWeek(self, ctx:FriendlyDateParser.DateRelativeYearWeekContext):
        r = self.visitChildren(ctx)
        r['rule'] = 'year_week'
        return r

    @trace
    def visitDateRelativeMonthDayPosition(self, ctx:FriendlyDateParser.DateRelativeMonthDayPositionContext):
        r = self.visitChildren(ctx)
        r['rule'] = 'month_day_position'
        return r

    @trace
    def visitDateRelativeYearDayPosition(self, ctx:FriendlyDateParser.DateRelativeYearDayPositionContext):
        r = self.visitChildren(ctx)
        r['rule'] = 'year_day_position'
        return r

    @trace
    def visitWeekDay(self, ctx:FriendlyDateParser.WeekDayContext):
        return {'weekday': ctx.value}

    @trace
    def visitLastR(self, ctx:FriendlyDateParser.LastRContext):
        return {'modifier': 'last'}

    @trace
    def visitNextR(self, ctx:FriendlyDateParser.NextRContext):
        return {'modifier': 'next'}

    @trace
    def visitThisR(self, ctx:FriendlyDateParser.ThisRContext):
        return {'modifier': 'this'}

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

        if r.get('day_position') is not None:
            return self._make_date_absolute_by_day_position(r)

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

        d = date(year, month, day)
        if (weekday := r.get('weekday')) is not None:
            if d.weekday() != weekday:
                raise ValueError(f"Invalid date: weekday value does not match date ({weekdays[weekday]} given but it is a {d.strftime('%A, %d %B %Y')})")

        return d

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

    def _make_date_absolute_by_day_position(self, r):
        day_position = r['day_position']
        weekday = r.get('weekday', None)
        year = r.get('year', self._now.year)
        month = r.get('month')
        month1, year1 = month, year # For checking if the day is out of range later

        if month is not None and (month == 0 or month > 12):
            raise ValueError("Invalid date: month value out of range")

        if day_position == -1:
            if month is None:
                year += 1
            elif month < 12:
                month += 1
            else:
                month = 1
                year += 1
            day_position = 0

        first_day = date(year, month or 1, 1)
        if weekday is None:
            d = first_day + timedelta(days=day_position-1)
        else:
            first_weekday = first_day.weekday()
            off = weekday - first_weekday
            if off < 0:
                off += 7
            d = first_day + timedelta(days=off + 7*(day_position-1))

        if d.year != year1 or (month1 is not None and d.month != month1):
            raise ValueError("Invalid date: day ordinal out of range")
        return d

    def _make_datetime_delta(self, l):
        r = { 'years': 0, 'months': 0, 'weeks': 0, 'days': 0,
              'hours': 0, 'minutes': 0, 'seconds': 0, 'microseconds': 0 }
        for d in l:
            for k, v in d.items():
                r[k] += v
        return relativedelta(**r)

    def _make_date_alone(self, r):
        d = r.get('date', self._now.date())
        if (delta := r.get('date_delta')) is None:
            return d

        if r.get('delta_before', False):
            d -= delta
        else:
            d += delta
        return d

    def _make_datetime(self, r):
        if (d := r.get('date')) is None:
            d = self._now
        else:
            t = r.get('time', datetime.min.time())
            d = datetime.combine(d, t)
        if (delta := r.get('datetime_delta')) is not None:
            if r.get('delta_before', False):
                d -= delta
            else:
                d += delta

        if (tz := r.get('tz')) is not None:
            assert d.tzinfo is None, "Internal error: datetime already has a timezone"
            d = tz.localize(d)
        elif d.tzinfo is None:
             if (tz := self._default_tz) is not None:
                 d = tz.localize(d)
        return d

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
        if rule == 'month_week':
            return self._make_date_relative_month_week(r, now)
        if rule == 'year_week':
            return self._make_date_relative_year_week(r, now)
        if rule == 'month_day_position':
            return self._make_date_relative_month_day_position(r, now)
        if rule == 'year_day_position':
            return self._make_date_relative_year_day_position(r, now)
        raise ValueError(f"Internal error: Invalid rule: {rule}")

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
        year = now.year
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
        year = now.year
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

    def _make_date_relative_month_week(self, r, now):
        if (month := r.get('month')) is None:
            d = date(now.year, now.month, 1)
            if r['modifier'] == 'last':
                d = d - relativedelta(months=1)
            elif r['modifier'] == 'next':
                d = d + relativedelta(months=1)
            r['year'] = d.year
            r['month'] = d.month
        else:
            if r['modifier'] == 'last':
                if month >= now.month:
                    r['year'] = now.year - 1
            elif r['modifier'] == 'next':
                if month <= now.month:
                    r['year'] = now.year + 1
        return self._make_date_absolute_by_week(r)

    def _make_date_relative_year_week(self, r, now):
        if r['modifier'] == 'last':
            r['year'] = now.year - 1
        elif r['modifier'] == 'next':
            r['year'] = now.year + 1
        return self._make_date_absolute_by_week(r)

    def _make_date_relative_month_day_position(self, r, now):
        if (month := r.get('month')) is None:
            d = date(now.year, now.month, 1)
            if r['modifier'] == 'last':
                d = d - relativedelta(months=1)
            elif r['modifier'] == 'next':
                d = d + relativedelta(months=1)
            r['year'] = d.year
            r['month'] = d.month
        else:
            if r['modifier'] == 'last':
                if month >= now.month:
                    r['year'] = now.year - 1
            elif r['modifier'] == 'next':
                if month <= now.month:
                    r['year'] = now.year + 1
        return self._make_date_absolute_by_day_position(r)

    def _make_date_relative_year_day_position(self, r, now):
        if r['modifier'] == 'last':
            r['year'] = now.year - 1
        elif r['modifier'] == 'next':
            r['year'] = now.year + 1
        return self._make_date_absolute_by_day_position(r)

    def _this_monday(self, date):
        return date - relativedelta(days=date.weekday())

    def _this_weekday(self, date, weekday):
        return date - relativedelta(days=date.weekday() - weekday)
