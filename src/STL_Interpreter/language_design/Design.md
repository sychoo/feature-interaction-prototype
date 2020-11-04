# STL Language Design Documentation

## Signal Input Format
JSON format

## Syntax

## Semantics
```
G[1, 2](distanceToEnemy() > 1)
```

## Structure

### Comments
- // single line comments
- /*
    multiline comments
*/

### var vs. val declaration
- var declares variables while val declares constants that are immutable

### Types

#### Primitives
- Int
- Float
- String
- Boolean

#### STL
- STL (STL Formula)
```scala
// declaration
var i: Int;
val j: String;

// allows redeclaration of variables
var i, j, k: STL; 

// assignment
var k = "Hello" 
val phi_1 = G[1, 10](DistanceToEnemy() < 1;
```
### Binary Operators (BinOp)
- \+
- \-
- \*
- \/
- ==
- !=
- \>
- \>=
- <
- <=

### Logic Operators (LogicOp)
- && (logic and)
- || (logic or)
- => (implies)
- ! (not/negation)

### STL Operators (STLOp)
[Wikipedia](https://en.wikipedia.org/wiki/Linear_temporal_logic)

#### Unary Operators
- X [\<time-start>] \<STL-formula>  (Next)
- F [\<time-start>, \<time-end>] \<STL-formula> (Eventually, In the Future, ♦ diamond symbol)
- G [\<time-start>, \<time-end>] \<STL-formula> (Globally, 􏰀 box symbol)

#### Binary Operators
- \<STL-formula> U [\<time-start>, \<time-end>] \<STL-formula> (Until)
- \<STL-formula> R [\<time-start>, \<time-end>] \<STL-formula> (Release)
- \<STL-formula> W [\<time-start>, \<time-end>] \<STL-formula> (Weak Until)
- \<STL-formula> M [\<time-start>, \<time-end>] \<STL-formula> (Strong Release)

#### Code Reuse
- import statement

#### Robustness Score
- Robust (Calculate Robustness Score)
- Other LTL operators
```
Robust(<STL-formula>, <signal>, <time-start>)
```

#### separator
- \; (optional if separated by new line character, required if code are on the same line)
- \n


**Important Notes**
- Note that both \n -- new line character and ; -- semicolon can separate values, expressions and statements
- Note that I don't have to worry about white spaces (other than \n -- new line character) in the Tools.get_raw_program_string, because the lexer will ignore them anyway.


#### Coding standard
Stringify:
Val: ( 1.5, "Float" )

to_str() class function is used to present output during program execution
__str__() is for debugging purpose, it is used to represent the object