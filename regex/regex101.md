# Regex101
Solutions for the regex101 quiz problems.  

## TASK 1. Word Boundries
### Check if a string contains the word word in it (case insensitive). If you have no idea, I guess you could try `/word/`.

### Solutions
| Author | Regex |  Length |
|--------|----------|--------|
|  Julkar9 | `/\bword\b/i`  | 11 |

## TASK 2. Word Boundries
### Use substitution to replace every occurrence of the word i with the word I (uppercase, I as in me). E.g.: i''m replacing it. am i not? -> I''m replacing it. am I not?. A regex match is replaced with the text in the Substitution field when using substitution.

### Solutions
| Author | Regex |  Length |
|--------|----------|--------|
|  Julkar9 | `s/\bi\b/I/g`  | 9 |

## TASK 2. Word Boundries
### Use substitution to replace every occurrence of the word i with the word I (uppercase, I as in me). E.g.: i''m replacing it. am i not? -> I''m replacing it. am I not?. A regex match is replaced with the text in the Substitution field when using substitution.

### Solutions
| Author | Regex |  Length |
|--------|----------|--------|
|  Julkar9 | `/[^AEIOUa-z\d\W_]/g`  | 19 |

## TASK 2. Word Boundries
### Count the number of integers in a given string. Integers are, for example: 1, 2, 65, 2579, etc.

### Solutions
| Author | Regex |  Length |
|--------|----------|--------|
|  Julkar9 | `/\d+/g`  | 6 |

## TASK 2. Word Boundries
### Find all occurrences of 4 or more whitespace characters in a row throughout the string.

### Solutions
| Author | Regex |  Length |
|--------|----------|--------|
|  Julkar9 | `/\s{4,}/g`  | 9 |

## TASK 2. Word Boundries
### Find all occurrences of 4 or more whitespace characters in a row throughout the string.

### Solutions
| Author | Regex |  Length |
|--------|----------|--------|
|  Julkar9 | `/\s{4,}/g`  | 9 |

 


