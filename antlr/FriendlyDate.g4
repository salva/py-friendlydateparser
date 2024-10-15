grammar FriendlyDate;

import Timezone;

friendlyDateTime : dateTime EOF ;

dateTime
    : (dateTimeDelta (BEFORE|AFTER))? (date (AT? time)? anyTz? | now)
    | dateTimeDelta ago
    ;

now : NOW ;

anyTz : tz | tzAbbreviation ;
tz : TIMEZONE ;
tzAbbreviation: TIMEZONE_ABBREVIATION ;

friendlyDate : dateAlone EOF ;

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
weeksDelta : zNumber (WEEK | WEEKS) ;
daysDelta : zNumber (DAY | DAYS) ;

hoursDelta : zNumber HOURS ;
minutesDelta : zNumber MINUTES ;
secondsDelta : qNumber (SECOND | SECONDS) ;

timeAbsolute
    : hour COLON minute (COLON second)? amPm?
    | hour HOURS ( minute MINUTES (second (SECONDS|SECOND))? )? amPm?
    ;

hour : twoDigitNumber ;

minute : twoDigitNumber ;

second : twoDigitFloatNumber ;

twoDigitFloatNumber : TWO_DIGIT_NUMBER | TWO_DIGIT_FLOAT_NUMBER ;

amPm : am | pm ;

am: AM;

pm: PM;

date : dateRelativeByDate | dateAbsolute ;

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

dateMonthAsName
    : (weekDay COMMA?)? dayAsNumber separator? monthAsName (separator? yearLong)?
    | (weekDay COMMA?)? monthAsName separator dayAsNumber (separator yearLong)?
    | yearLong separator monthAsName separator dayAsNumber
    | THE? (dayAsOrdinal | lastDay) OF monthAsName ((COMMA|OF)? yearLong)?
    | monthAsName dayAsNumberOrOrdinal  (','? yearLong)?
    | monthAsName (separator? yearLong)?
    ;

lastDay : LAST DAY;

dateMonthAsNumber
    : (weekDay COMMA?)? twoDigitNumberLeft separator twoDigitNumberRight (separator yearLong)?
    | yearLong separator monthAsNumber separator dayAsNumber
    | monthAsNumber separator yearLong
    ;

dateWithWeek
    : THE?
        ( weekDay OF? )?
        ( weekNumber
            (OF?
                ( monthAsNameOrNumber separator yearLong
                | monthAsName (OF? yearLong)?
                | yearLong
                )
            )?
        | lastWeek
            (OF?
                ( monthAsNameOrNumber separator yearLong
                | monthAsName (OF? yearLong)?
                | yearLong
                )
            )
        )
    ;

dateWithDayPosition
    : THE?
        (weekDayPositionOrdinal | weekDayPositionLast | dayPositionNumber)
        (OF?
            ( monthAsNameOrNumber separator yearLong
            | monthAsName (OF? yearLong)?
            | yearLong
            )
        )
    ;

weekDayPositionOrdinal : dayPositionOrdinal (DAY | weekDay) ;

weekDayPositionLast : LAST weekDay ;

dayPositionNumber : DAY anyDigitNumber ;

dayPositionOrdinal : anyOrdinal ;

lastWeek: LAST WEEK;

weekNumber : WEEK twoDigitNumber ;

twoDigitNumberLeft : twoDigitNumber ;

twoDigitNumberRight : twoDigitNumber ;

dateLongNumber : EIGHT_DIGIT_NUMBER ;

dateYear : (THE? lastDay OF)? yearLong;

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

dayAsNumberOrOrdinal : dayAsNumber | dayAsOrdinal ;

dayAsOrdinal : anyOrdinal ;

anyOrdinal : twoDigitOrdinal | wordOrdinal ;

twoDigitOrdinal : ORDINAL_DIGITS ;

wordOrdinal : ORDINAL_WORDS | SECOND;

monthAsNumber : twoDigitNumber ;

dayAsNumber : twoDigitNumber ;

yearLong : fourDigitNumber ;

fourDigitNumber : FOUR_DIGIT_NUMBER ;

twoDigitNumber : TWO_DIGIT_NUMBER ;

zNumber : (MINUS|PLUS)? anyDigitNumber ;

qNumber : (MINUS|PLUS)? anyFloatNumber ;

anyFloatNumber : TWO_DIGIT_FLOAT_NUMBER | ANY_DIGIT_FLOAT_NUMBER | anyDigitNumber;

anyDigitNumber : TWO_DIGIT_NUMBER | FOUR_DIGIT_NUMBER | EIGHT_DIGIT_NUMBER | ANY_DIGIT_NUMBER ;

// threeDigitNumber : TWO_DIGIT_NUMBER | THREE_DIGIT_NUMBER ;

weekDay returns [value]
    : MON {$value = 0;}
    | TUE {$value = 1;}
    | WED {$value = 2;}
    | THU {$value = 3;}
    | FRI {$value = 4;}
    | SAT {$value = 5;}
    | SUN {$value = 6;}
    ;

separator : MINUS | SLASH;

fragment DIGIT : [0-9] ;

TWO_DIGIT_FLOAT_NUMBER : DIGIT? DIGIT '.' DIGIT* ;

ANY_DIGIT_FLOAT_NUMBER : DIGIT+ '.' DIGIT* ;

TWO_DIGIT_NUMBER : DIGIT DIGIT? ;

FOUR_DIGIT_NUMBER : [0-9] [0-9] [0-9] [0-9] ;

EIGHT_DIGIT_NUMBER : [0-9] [0-9] [0-9] [0-9] ( '0' [1-9] | '1' [0-2] ) ( '0' [1-9] | [1-2] [0-9] | '3' [0-1] ) ;

ANY_DIGIT_NUMBER : DIGIT+ ;

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


YEARS : 'y' | 'ys' | 'years' ;
MONTHS : 'mo' | 'mos'| 'months' ;
WEEKS : 'w' | 'ws' | 'weeks' ;
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
MINUS : '-';
SLASH : '/';

WS : [ \t\r\n]+ -> skip ;
