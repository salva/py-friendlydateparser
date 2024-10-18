grammar FriendlyDate;

import Timezone, Unknown;

friendlyDateTime : dateTime EOF ;

dateTime
    : (dateTimeDelta (BEFORE|AFTER))?
        (date (AT? time)? anyTz?
        | iso8601DateTime
        | now )
    | dateTimeDelta ago
    ;

now : NOW ;

anyTz : tz | tzAbbreviation | tzOffset;
tz : TIMEZONE ;
tzAbbreviation: TIMEZONE_ABBREVIATION ;
tzOffset : (DASH | PLUS) hour12 (COLON? minute2)? ;

friendlyDate : dateAlone EOF ;

friendlyTimezone : (tzZ | anyTz) ;

dateAlone
    : (dateDelta (before|after))? date
    | dateDelta ago
    ;

before : BEFORE ;
after : AFTER ;
ago : AGO ;

time
    : timeAbsolute
    | midnight
    | noon
    ;

midnight : MIDNIGHT ;

noon : NOON | MIDDAY ;

dateDelta
    : (yearsDelta | monthsDelta | weeksDelta |daysDelta )
        (COMMA? (yearsDelta | monthsDelta | weeksDelta | daysDelta ))*
    ;

dateTimeDelta
    : (yearsDelta | monthsDelta | weeksDelta | daysDelta | hoursDelta | minutesDelta | secondsDelta)
        (COMMA? (yearsDelta | monthsDelta | weeksDelta | daysDelta | hoursDelta | minutesDelta | secondsDelta))*
    ;

yearsDelta : zNumber (YEAR | YEARS) ;
monthsDelta : zNumber (MONTH | MONTHS) ;
weeksDelta : zNumber (W | WEEK | WEEKS) ;
daysDelta : zNumber (DAY | DAYS) ;

hoursDelta : zNumber HOURS ;
minutesDelta : zNumber MINUTES ;
secondsDelta : qNumber (SECOND | SECONDS) ;

timeAbsolute
    : hour12 COLON minute2 (COLON second2)? amPm?
    | hour12 HOURS ( minute12 MINUTES (second12 (SECONDS|SECOND))? )? amPm?
    ;

hour12 : number12 ;
minute12 : number12 ;
second12: float12 ;

hour2 : number2 ;
minute2 : number2 ;
second2 : float2 ;

amPm : am | pm ;
am: AM;
pm: PM;

date : dateRelativeByDate | dateAbsolute | iso8601Date;

dateRelativeByDate : dateRelative (BY date)? ;

dateRelative
    : today
    | yesterday
    | tomorrow
    | theDayAfterTomorrow
    | theDayBeforeYesterday
    | dateRelativeDay
    | dateRelativeWeek
    | dateRelativeMonth
    | dateRelativeYearWithoutMonth
    | dateRelativeYearWithMonth
    | dateRelativeMonthWeek
    | dateRelativeYearWeek
    | dateRelativeMonthDayPosition
    | dateRelativeYearDayPosition
    ;

today : TODAY ;

yesterday : YESTERDAY ;

tomorrow : TOMORROW ;

theDayBeforeYesterday : THE DAY BEFORE YESTERDAY ;

theDayAfterTomorrow : THE DAY AFTER TOMORROW ;

dateRelativeDay : (lastR | nextR | thisR)? weekDay ;

dateRelativeWeek : (weekDay OF?)? (lastR | nextR | thisR) WEEK ;

dateRelativeMonth : (THE? (dayAsOrdinal | lastDay) OF)? (lastR | nextR | thisR) (MONTH | monthAsName) ;

dateRelativeYearWithMonth : (THE? (dayAsOrdinal | lastDay) OF)? monthAsName (COMMA|OF)?  (lastR | nextR | thisR) YEAR ;

dateRelativeYearWithoutMonth : (THE? lastDay OF)? (lastR | nextR | thisR) YEAR ;

dateRelativeMonthWeek
    : THE?
        ( weekDay OF? )?
        ( weekNumber | lastWeek )
        OF? (lastR|nextR|thisR) (MONTH | monthAsName)
    ;

dateRelativeYearWeek
    : THE?
        ( weekDay OF? )?
        ( weekNumber | lastWeek )
        (OF? monthAsName)?
        OF? (lastR|nextR|thisR) YEAR
    ;

dateRelativeMonthDayPosition
    : THE?
        ( weekDayPositionOrdinal | weekDayPositionLast | dayPositionNumber )
        OF? (lastR|nextR|thisR) (MONTH | monthAsName)
    ;

dateRelativeYearDayPosition
    : THE?
        ( weekDayPositionOrdinal | weekDayPositionLast | dayPositionNumber )
        (OF? monthAsName)?
        OF? (lastR|nextR|thisR) YEAR
    ;

lastR : LAST ;
nextR : NEXT | THIS COMMING ;
thisR : THIS ;

last : LAST ;

dateAbsolute
    : dateMonthAsName
    | dateMonthAsNumber
    | dateYear
    | dateWithWeek
    | dateWithDayPosition
    | dateLongNumber
    ;

iso8601DateTime : iso8601Date T iso8601Time iso8601Tz ;

iso8601Time : hour2 COLON minute2 (COLON second2)? ;

iso8601Tz : tzZ | tzOffset ;

tzZ : Z ;

iso8601Date
    : iso8601DateStandard
    | iso8601DateWeek
    | iso8601DateDay
    ;

iso8601DateStandard : year4 DASH monthAsNumber DASH dayAsNumber ;
iso8601DateWeek : year4 DASH W iso8601YearWeek DASH iso8601WeekDay ;
iso8601DateDay : year4 DASH iso8601YearDay ;

iso8601Month : number2 ;
iso8601MonthDay : number2 ;
iso8601YearWeek : number2 ;
iso8601WeekDay : number1 ;
iso8601YearDay : number3 ;

dateMonthAsName
    : (weekDay COMMA?)? dayAsNumber separator? monthAsName (separator? year4)?
    | (weekDay COMMA?)? monthAsName separator dayAsNumber (separator year4)?
    | year4 separator monthAsName separator dayAsNumber
    | THE? (dayAsOrdinal | lastDay) OF monthAsName ((COMMA|OF)? year4)?
    | monthAsName dayAsNumberOrOrdinal  (','? year4)?
    | monthAsName (separator? year4)?
    ;

lastDay : LAST DAY;

dateMonthAsNumber
    : (weekDay COMMA?)? number12Left separator number12Right (separator year4)?
    | year4 separator monthAsNumber separator dayAsNumber
    | monthAsNumber separator year4
    ;

dateWithWeek
    : THE?
        ( weekDay OF? )?
        ( weekNumber
            (OF?
                ( monthAsNameOrNumber separator year4
                | monthAsName (OF? year4)?
                | year4
                )
            )?
        | lastWeek
            (OF?
                ( monthAsNameOrNumber separator year4
                | monthAsName (OF? year4)?
                | year4
                )
            )
        )
    ;

dateWithDayPosition
    : THE?
        (weekDayPositionOrdinal | weekDayPositionLast | dayPositionNumber)
        (OF?
            ( monthAsNameOrNumber separator year4
            | monthAsName (OF? year4)?
            | year4
            )
        )
    ;

weekDayPositionOrdinal : dayPositionOrdinal (DAY | weekDay) ;

weekDayPositionLast : LAST weekDay ;

dayPositionNumber : DAY number ;

dayPositionOrdinal : anyOrdinal ;

lastWeek: LAST WEEK;

weekNumber : WEEK number12 ;

number12Left : number12 ;

number12Right : number12 ;

dateLongNumber : EIGHT_DIGIT_NUMBER ;

dateYear : (THE? lastDay OF)? year4;

monthAsNameOrNumber : monthAsNumber | monthAsName ;

monthAsName returns [value]
    : JAN {$value =  1;}
    | FEB {$value =  2;}
    | MAR {$value =  3;}
    | APR {$value =  4;}
    | MAY {$value =  5;}
    | JUN {$value =  6;}
    | JUL {$value =  7;}
    | AUG {$value =  8;}
    | SEP {$value =  9;}
    | OCT {$value = 10;}
    | NOV {$value = 11;}
    | DEC {$value = 12;}
    ;

weekDay returns [value]
    : MON {$value = 0;}
    | TUE {$value = 1;}
    | WED {$value = 2;}
    | THU {$value = 3;}
    | FRI {$value = 4;}
    | SAT {$value = 5;}
    | SUN {$value = 6;}
    ;

separator : DASH | SLASH;

dayAsNumberOrOrdinal : dayAsNumber | dayAsOrdinal ;

dayAsOrdinal : anyOrdinal ;

anyOrdinal : ordinalDigits | wordOrdinal ;

ordinalDigits : ORDINAL_DIGITS ;

wordOrdinal : ORDINAL_WORDS | SECOND;

monthAsNumber : number12 ;

dayAsNumber : number12 ;

year4 : number4 ;


number1 : ONE_DIGIT_NUMBER ;
number2 : TWO_DIGIT_NUMBER ;
number12 : number1 | number2 ;
number3 : THREE_DIGIT_NUMBER ;
number4 : FOUR_DIGIT_NUMBER ;
number : ONE_DIGIT_NUMBER | TWO_DIGIT_NUMBER | THREE_DIGIT_NUMBER | FOUR_DIGIT_NUMBER | EIGHT_DIGIT_NUMBER | ANY_DIGIT_NUMBER ;


float1 : ONE_DIGIT_FLOAT_NUMBER | ONE_DIGIT_FLOAT_NUMBER ;
float2 : TWO_DIGIT_FLOAT_NUMBER | TWO_DIGIT_NUMBER ;
float12 : float1 | float2 ;
float : ONE_DIGIT_FLOAT_NUMBER | TWO_DIGIT_FLOAT_NUMBER | ANY_DIGIT_FLOAT_NUMBER | number;


zNumber : (DASH|PLUS)? number;
qNumber : (DASH|PLUS)? float;


fragment DIGIT : [0-9] ;

ONE_DIGIT_NUMBER : DIGIT ;

TWO_DIGIT_NUMBER : DIGIT DIGIT ;

THREE_DIGIT_NUMBER : DIGIT DIGIT DIGIT ;

FOUR_DIGIT_NUMBER : DIGIT DIGIT DIGIT DIGIT ;

EIGHT_DIGIT_NUMBER : [0-9] [0-9] [0-9] [0-9] ( '0' [1-9] | '1' [0-2] ) ( '0' [1-9] | [1-2] [0-9] | '3' [0-1] ) ;

ANY_DIGIT_NUMBER : DIGIT+ ;

ONE_DIGIT_FLOAT_NUMBER : DIGIT '.' DIGIT* ;

TWO_DIGIT_FLOAT_NUMBER : DIGIT DIGIT '.' DIGIT* ;

ANY_DIGIT_FLOAT_NUMBER : DIGIT+ '.' DIGIT* ;

JAN : 'jan' ('uary')? ;
FEB : 'feb' ('ruary')? ;
MAR : 'mar' ('ch')? ;
APR : 'apr' ('il')? ;
MAY : 'may' ;
JUN : 'jun' ('e')? ;
JUL : 'jul' ('y')? ;
AUG : 'aug' ('ust')? ;
SEP : 'sep' ('tember')? ;
OCT : 'oct' ('ober')? ;
NOV : 'nov' ('ember')? ;
DEC : 'dec' ('ember')? ;

MON : 'mon' ('day')? ;
TUE : 'tue' ('sday')? ;
WED : 'wed' ('nesday')? ;
THU : 'thu' ('rsday')? ;
FRI : 'fri' ('day')? ;
SAT : 'sat' ('urday')? ;
SUN : 'sun' ('day')? ;

THE : 'the';
OF : 'of';
IN : 'in';
AT : 'at';
BY : 'by';

TODAY : 'today';
TOMORROW : 'tomorrow';
YESTERDAY : 'yesterday';
NOW : 'now';
AGO : 'ago';

COMMA : ',';
COLON : ':';
SEMICOLON : ';';

LAST : 'last';
NEXT : 'next';
THIS : 'this';
COMMING : 'comming';

FROM : 'from';
AFTER : 'after';
BEFORE : 'before';

SECOND: 'second';

HOURS: 'h' ('r' | 'ours')? 's'?;
MINUTES: 'm' ('in' | 'inute')? 's'?;
SECONDS: 's' 'ec'? 's'? | 'seconds';

AM : 'am';
PM : 'pm';

MIDNIGHT : 'midnight';
NOON : 'noon';
MIDDAY : 'midday';

END : 'end';
BEGINNING : 'beginning';

DAY : 'day';
WEEK : 'week';
MONTH : 'month';
YEAR : 'year';

W : 'w';
T : 't';
Z : 'z';

YEARS : 'y' | 'ys' | 'years' ;
MONTHS : 'mo' | 'mos'| 'months' ;
WEEKS : 'ws' | 'weeks' ;
DAYS : 'd' | 'ds' | 'days' ;

ORDINAL_DIGITS
    : ([1-9][0-9]?)? '1st'
    | ([1-9][0-9]?)? '2nd'
    | ([1-9][0-9]?)? '3rd'
    | ([1-9][0-9]?)? [4-9] 'th'
    | [1-9][0-9]? '0th'
    ;

ORDINAL_WORDS
    : 'first'
    // | 'second',  --Nope, it has its own rule
    | 'third'
    | ('four' | 'fif' | 'six' | 'seven' | 'eight' | 'nine' | 'ten' | 'eleven' | 'twel') 'th'
    | ('thir' | 'four' | 'fif' | 'six' | 'seven' | 'eight' | 'nine') 'teenth'
    | ('twent' | 'thirt' | 'fort' | 'fift' | 'sixt' | 'sevent' | 'eight' | 'ninet') 'ieth'
    | ('twenty' | 'thirty' | 'forty' | 'fifty' | 'sixty' | 'seventy' | 'eighty' | 'ninety')
        '-'
        ('first' | 'second' | 'third' | 'fourth' | 'fifth' | 'sixth' | 'seventh' | 'eighth' | 'ninth')
    ;

PLUS : '+';
DASH : '-';
SLASH : '/';

WS : [ \t\r\n]+ -> skip ;
