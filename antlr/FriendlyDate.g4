grammar FriendlyDate;

friendlyDateTime : dateTime EOF ;

dateTime : date atTime? ;

atTime : AT? time ;

friendlyDate : date EOF ;

friendlyTime : time EOF ;

time
    : timeAbsolute
    | midnight
    | noon
    | timeNow
    ;

midnight : MIDNIGHT ;

noon : NOON | MIDDAY ;

timeNow : NOW ;

timeAbsolute
    : hour COLON minute (COLON second)? amPm?
    | hour H ( minute M (second S)? )? amPm?
    ;

hour : twoDigitNumber ;

minute : twoDigitNumber ;

second
    : twoDigitFloatNumber
    ;

twoDigitFloatNumber
    : TWO_DIGIT_NUMBER
    | TWO_DIGIT_FLOAT_NUMBER
    ;

amPm : am | pm ;

am: AM;

pm: PM;

date : dateAbsolute | dateRelative ;

dateRelative
    : today
    | dateRelativeDay
    | dateRelativeWeek
    | dateRelativeMonth
    | dateRelativeYearWithoutMonth
    | dateRelativeYearWihMonth
    ;

today : TODAY ;

dateRelativeDay : (LAST | NEXT | THIS)? weekDay ;

dateRelativeWeek : weekDay (LAST | NEXT | THIS) WEEK ;

dateRelativeMonth : (THE? (dayAsOrdinal | END) OF)? (LAST | NEXT | THIS) (MONTH | monthAsName) ;

dateRelativeYearWihMonth : THE? (dayAsOrdinal | END) OF monthAsName (COMMA|OF)?  (LAST | NEXT | THIS) YEAR ;

dateRelativeYearWithoutMonth : (THE? END OF)? (LAST | NEXT | THIS) YEAR ;

dateAbsolute
    : dateMonthAsName
    | dateMonthAsNumber
    | dateLongNumber
    | yearLong
    ;

dateMonthAsName
    : dayAsNumber SEPARATOR? monthAsName (SEPARATOR? yearLong)?
    | monthAsName SEPARATOR dayAsNumber (SEPARATOR yearLong)?
    | yearLong SEPARATOR monthAsName SEPARATOR dayAsNumber
    | THE? (dayAsOrdinal | END) OF monthAsName ((COMMA|OF)? yearLong)?
    | monthAsName dayAsNumberOrOrdinal  (','? yearLong)?
    | monthAsName (SEPARATOR? yearLong)?
    ;

dateMonthAsNumber
    : twoDigitNumberLeft SEPARATOR twoDigitNumberRight (SEPARATOR yearLong)?
    | yearLong SEPARATOR monthAsNumber SEPARATOR dayAsNumber
    | monthAsNumber SEPARATOR yearLong
    ;

twoDigitNumberLeft : twoDigitNumber ;

twoDigitNumberRight : twoDigitNumber ;

dateLongNumber : YEAR_MONTH_DAY ;

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

dayAsOrdinal : DAY_AS_ORDINAL ;

monthAsNumber : twoDigitNumber ;

dayAsNumber : twoDigitNumber ;

yearLong : fourDigitNumber ;

fourDigitNumber : FOUR_DIGIT_NUMBER ;

twoDigitNumber : TWO_DIGIT_NUMBER ;

weekDay returns [value]
    : MON {$value = 1;}
    | TUE {$value = 2;}
    | WED {$value = 3;}
    | THU {$value = 4;}
    | FRI {$value = 5;}
    | SAT {$value = 6;}
    | SUN {$value = 7;}
    ;

TWO_DIGIT_FLOAT_NUMBER : [0-9]?[0-9] '.' [0-9]* ;

TWO_DIGIT_NUMBER : [0-9] [0-9]? ;

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

TODAY : 'today';
NOW : 'now';

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

H: 'h' ('r' | 'ours')? 's'?;
M: 'm' ('in' | 'inute')? 's'?;
S: 's' ('ec' | 'econd')? 's'?;

AM : 'am';
PM : 'pm';

MIDNIGHT : 'midnight';
NOON : 'noon';
MIDDAY : 'midday';

END : 'end';
BEGINNING : 'beginning';

WEEK : 'week';
MONTH : 'month';
YEAR : 'year';

DAY_AS_ORDINAL
    : '1st'
    | '2nd'
    | '3rd'
    | '4th' | '5th' | '6th' | '7th' | '8th' | '9th'
    | '10th' | '11th' | '12th' | '13th' | '14th' | '15th' | '16th' | '17th' | '18th' | '19th' | '20th'
    | '21st'
    | '22nd'
    | '23rd'
    | '24th' | '25th' | '26th' | '27th' | '28th' | '29th' | '30th'
    | '31st'
    ;

FOUR_DIGIT_NUMBER : [0-9] [0-9] [0-9] [0-9] ;

YEAR_MONTH_DAY : [0-9] [0-9] [0-9] [0-9] ( '0' [1-9] | '1' [0-2] ) ( '0' [1-9] | [1-2] [0-9] | '3' [0-1] ) ;

SEPARATOR : '/' | '-';

WS : [ \t\r\n]+ -> skip ;
