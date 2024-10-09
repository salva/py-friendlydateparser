from .FriendlyDateVisitor import FriendlyDateVisitor
from .FriendlyDateParser import FriendlyDateParser
import functools
from datetime import datetime
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

class FriendlyDateVisitorPy(FriendlyDateVisitor):
    def __init__(self, now, month_first, _trace_visiting=False):
        assert isinstance(now, datetime), "now must be a datetime object"
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
    def make_date(self, ctx):
        try:
            day, month, year = self.visit(ctx)
        except Exception as e:
            logging.exception(e)
            raise Exception(f"Error parsing date: {ctx.toStringTree(recog=ctx.parser)}") from e

        if day is None:
            day = 1
        if month is None:
            month = 1
        if year is None:
            year = self._now.year

        return datetime(year, month, day)

    @trace
    def visitFriendlyDate(self, ctx:FriendlyDateParser.FriendlyDateContext):
        return self.visitDateExpression(ctx.dateExpression())

    @trace
    def visitDmyMonthAsName(self, ctx:FriendlyDateParser.DmyMonthAsNameContext):
        if (c := ctx.dayAsNumber()):
            day = self.visitDayAsNumber(c)
        elif (c := ctx.dayAsOrdinal()):
            day = self.visitDayAsOrdinal(c)
        else:
            day = None

        month = self.visitMonthAsName(ctx.monthAsName())

        if (c := ctx.yearLong()):
            year = self.visitYearLong(c)
        else:
            year = None

        return (day, month, year)

    @trace
    def visitDmyMonthAsNumber(self, ctx:FriendlyDateParser.DmyMonthAsNumberContext):
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

        return (day, month, year)

    @trace
    def visitDmyYearAlone(self, ctx:FriendlyDateParser.DmyYearAloneContext):
        year = self.visitYearLong(ctx.yearLong())
        return (None, None, year)

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
    def visitRelativeDate(self, ctx:FriendlyDateParser.RelativeDateContext):
        return (None, None, None) # TODO

