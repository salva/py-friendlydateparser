"""
Friendly Date Parser - A Python library for parsing human-readable date and time expressions.
"""

import friendlydateparser.antlr.FriendlyDateLexer

from antlr4 import InputStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener
from friendlydateparser.antlr.FriendlyDateLexer import FriendlyDateLexer
from friendlydateparser.antlr.FriendlyDateParser import FriendlyDateParser
from friendlydateparser.antlr.FriendlyDateVisitorPy import FriendlyDateVisitorPy

from datetime import datetime, date
import logging

def _resolve_now(now, default_tz):
    if now is None:
        return datetime.now()
    if isinstance(now, str):
        return parse_datetime(now, default_tz=default_tz)
    if isinstance(now, datetime):
        return now
    if isinstance(now, date):
        return datetime.combine(now, datetime.min.time())
    raise ValueError("Invalid value for 'now' parameter")

def _resolve_month_first(month_first):
    if month_first is None:
        return True
    if month_first == "locale":
        import locale
        date_format = locale.nl_langinfo(locale.D_FMT)
        return date_format.startswith('%m')
    return month_first

def _resolve_tz(tz):
    if tz is None:
        return None
    if isinstance(tz, str):
        return parse_timezone(tz)
    return tz

def _parse_anything(text, what, now=None, month_first=True, default_tz=None):
    default_tz = _resolve_tz(default_tz)
    now = _resolve_now(now, default_tz)
    month_first = _resolve_month_first(month_first)
    input_stream = InputStream(text.lower())
    lexer = FriendlyDateLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = FriendlyDateParser(token_stream)
    error_listener = _ErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)

    if what == "date":
        tree = parser.friendlyDate()
    elif what == "datetime":
        tree = parser.friendlyDateTime()
    elif what == "timezone":
        tree = parser.friendlyTimezone()
    else:
        raise ValueError(f"Invalid value for 'what' parameter: {what}")

    if error_listener.count > 0:
        raise ValueError(f"Invalid {what} '{text}', {error_listener.first_error()}, partial result: {tree.toStringTree(recog=parser)}")

    visitor = FriendlyDateVisitorPy(now=now, month_first=month_first, default_tz=default_tz)
    return visitor.visit(tree)

def parse_date(text, now=None, month_first=True):
    return _parse_anything(text, "date", now=now, month_first=month_first)

def parse_datetime(text, now=None, month_first=True, default_tz=None):
    return _parse_anything(text, "datetime", now=now, month_first=month_first, default_tz=default_tz)

def parse_timezone(text):
    return _parse_anything(text, "timezone")

class _ErrorListener(ErrorListener):
    def __init__(self):
        self.errors = []
        self.count = 0

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(f"Syntax error at line {line}, column {column}: {msg}")
        self.count += 1

    def first_error(self):
        if len(self.errors) > 0:
            return self.errors[0]
        return None
