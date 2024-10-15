#!/usr/bin/env python3

import pytz

from src.friendlydateparser.tz_abbreviations import tz_abbreviations

abbreviations = "'\n    | '" .join([x.lower() for x in tz_abbreviations.keys()
                                    if x not in pytz.all_timezones])

tza = "'\n    | '".join([x.lower() for x in pytz.all_timezones])

print(f"""
grammar Timezone;

TIMEZONE
    : '{tza}'
    ;

TIMEZONE_ABBREVIATION
    : '{abbreviations}'
    ;

""")
