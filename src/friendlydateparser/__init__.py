import friendlydateparser.antlr.FriendlyDateLexer

from antlr4 import InputStream, CommonTokenStream
from friendlydateparser.antlr.FriendlyDateLexer import FriendlyDateLexer
from friendlydateparser.antlr.FriendlyDateParser import FriendlyDateParser
from friendlydateparser.antlr.FriendlyDateVisitorPy import FriendlyDateVisitorPy

from datetime import datetime

def _resolve_now(now):
    if now is None:
        return datetime.now()
    if isinstance(now, str):
        return parse_date(now)
    if isinstance(now, datetime):
        return now
    raise ValueError("Invalid value for 'now' parameter")

def _resolve_month_first(month_first):
    if month_first is None:
        return True
    if month_first == "locale":
        import locale
        date_format = locale.nl_langinfo(locale.D_FMT)
        return date_format.startswith('%m')
    return month_first

def parse_date(text, now=None, month_first=True):

    now = _resolve_now(now)
    month_first = _resolve_month_first(month_first)

    input_stream = InputStream(text.lower())
    lexer = FriendlyDateLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = FriendlyDateParser(token_stream)

    tree = parser.friendlyDate()
    visitor = FriendlyDateVisitorPy(now=now, month_first=month_first, _trace_visiting=True)
    result = visitor.make_date(tree)

    return result
