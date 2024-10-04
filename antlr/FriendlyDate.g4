grammar FriendlyDate;

dateExpression
    : dayMonthAndYear
    | relativeDate
    ;

// october/3/2017
// october/3
// 3/october/2017
// 3/october
// 10/3/2017
// 10/3
// october/2017
// 10/2017
// october
// the third of october, 2017
// the third of october 2017
// the third of october

// Relative Dates (e.g., "last Monday", "next Fri")
relativeDate
    : ('last' | 'next' | ('this' ('comming')?) ) dayOfWeek
    ;

dayMonthAndYear
returns [day, month, year, ambiguous]
    : sd=spokenDate
        {$day, $month, $year, $ambiguous = $day, $month, $year, False;}
    | dmyf=dayMonthAndYearFormal
        {$day, $month, $year, $ambiguous = $dmyf.day, $dmyf.month, $dmyf.year, False;}
    | dam=dayAndMonth SEPARATOR y=yearLong
        {$day, $month, $year, $ambiguous = $dam.day, $dam.month, $y.value, $dam.ambiguous;}
    | dam1=dayAndMonth
        {$day, $month, $year, $ambiguous = $dam1.day, $dam1.month, None, $dam1.ambiguous;}
    | mbn=monthByName
        {$day, $month, $year, $ambiguous = None, $mbn.value, None, False;}
    ;

reverseDate
returns [day, month, year, ambiguous]
    : y=yearLong SEPARATOR m=monthByNameOrNumber SEPARATOR d=dayAsNumber
        {$day, $month, $year = $d.value, $m.value, $y.value;}
    | YEARMONTHDAY
        {$day, $month, $year = int($YEARMONTHDAY.text.substring(6, 8)), int($YEARMONTHDAY.text.substring(4, 6)), int($YEARMONTHDAY.text.substring(0, 4));}
    ;

// Spoken Dates (e.g., "the third of october")
spokenDate
returns [day, month, year]
    : 'the' d0=dayAsOrdinal 'of' m0=monthByName
        {$day, $month, $year = $d0.value, $m0.value, None;}
    | 'the' d1=dayAsOrdinal 'of' m1=monthByName 'in'? y1=yearLong
        {$day, $month, $year = $d1.value, $m1.value, $y1.value;}
    ;

// october/3
// 3/october
// 10/3
dayAndMonth
returns [day, month, ambiguous]
    : m0=monthByName
        {$day, $month, $ambiguous = None, $m0.value, False;}
    | m1=monthByName SEPARATOR d1=dayAsNumber
        {$day, $month, $ambiguous = $d1.value, $m1.value, False;}
    | d2=dayAsNumber SEPARATOR m2=monthByName
        {$day, $month, $ambiguous = $d2.value, $m2.value, False;}
    | m3=dayAsNumber SEPARATOR d3=dayAsNumber
        {$day, $month, $ambiguous = $d3.value, $m3.value, True;}
    ;

dayMonthAndYearFormal returns [day, month, year]
    : m=monthByName d=dayOrOrdinal  (','? y=yearLong)?
        {$day, $month, $year = $m.value, $d.value, $y.value;}
    ;

yearLong returns [value]
    : YEAR {$value = int($YEAR.text);}
    ;

monthByNameOrNumber returns [value]
    : monthByNumber {$value = $monthByNumber.value;}
    | monthByName   {$value = $monthByName.value;}
    ;

monthByName returns [value]
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

monthByNumber returns [value]
    : MONTH_BY_NUMBER {$value = int($MONTH_BY_NUMBER.text);}
    ;

dayAsNumber returns [value]
    : DAY {$value = int($DAY.text);}
    ;

dayOrOrdinal returns [value]
    : dayAsNumber {$value = $dayAsNumber.value;}
    | dayAsOrdinal {$value = $dayAsOrdinal.value;}
    ;

dayOfWeek returns [value]
    : MON {$value = 1;}
    | TUE {$value = 2;}
    | WED {$value = 3;}
    | THU {$value = 4;}
    | FRI {$value = 5;}
    | SAT {$value = 6;}
    | SUN {$value = 7;}
    ;

dayAsOrdinal returns [value]
    : DAY_AS_ORDINAL {$value = int($DAY_AS_ORDINAL.text[:-2])}
    ;

// Lexer rules for valid days (1-31)
DAY
    : '0'?[1-9]     // 01-09, 1-9
    | '1'[0-9]      // 10-19
    | '2'[0-9]      // 20-29
    | '3'[01]       // 30-31
    ;

// Valid month range (1-12)
MONTH_BY_NUMBER
    : '0'?[1-9]     // 01-09, 1-9
    | '1'[0-2]      // 10-12
    ;

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

// Force year to be 4 digits
YEAR
    : [0-9] [0-9] [0-9] [0-9]  // Must be exactly 4 digits
    ;

YEARMONTHDAY
    : [0-9] [0-9] [0-9] [0-9] ( '0' [1-9] | '1' [0-2] ) ( '0' [1-9] | [1-2] [0-9] | '3' [0-1] )
    ;

SEPARATOR : '/' | '-';

// Lexer for numbers and whitespace
WS : [ \t\r\n]+ -> skip ;
