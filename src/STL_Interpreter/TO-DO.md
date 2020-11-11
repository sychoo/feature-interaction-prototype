DONE: 
- [X] check the suffix of the program supplied
- [X] can't loop through token stream - make a copy of the token stream and detect the number of tokens

TO-DO:
- [ ] context and scoping
- [ ] encode STL
- [ ] handle empty input
- [ ] extract raw program string from string (Tools)
- [ ] problem with unittesting - cannot run the program standalone, must use external file for some reason
        - cannot captures standard output
- [ ] figure out why print2 and print3 doesn't work

- [ ] standardize the signal format, have a signal type (regex match JSON?)

- [ ] apply keyword: apply(<STL-formula>, <Signal>).eval()
                     apply(<STL-formula>, <Signal>).robustness()

- [X] resolve block issue - got rid of block
- [X] signal parsing issue (can't parser JSON correctly) ${}$

- define __ne__ __add__ operators for the primitive types associated with the first operand

- overload comparison and logical oeprators

- typecheck

- maybe move the separator to the statement  in the parser
- stmt_list : stmt_list separator stmt

maybe bad idea, do some preprocessing, and make sure :::NO
instead to prevent test_error/bin_op.stl
        - caused by no separator

- add unary arithmetic operators

- boolean logic operators


Finished!
- [X] Boolean Logical expressions (both unary and binary)





Task for Saturday, 10/7/2020


- signal evaluation using STL formulas
        - standardize signal formats
        - evaluation functions for different STL formulas


- type check (type context)
- val and var declaration (don't allow redeclaration?)
- evaluation of variable formulas (eval context)
- create type for each primitive values (as separate classes)

- RESTRICTIONS: limit the update of the context according to the 
        - val decl
        - type tags!

- RESTRICTIONS: do not allow re-assignment for val declaration
        - implement var declaration first
        
  - RESTRICTIONS
  	- make sure none of the variable identifiers are declared prior to the VAR or VAL declaration

- RESTRICTIONS:
        - DO NOT ALLOW REDECLARATINO of VARIABLES (with the same identifier)
- block statement?

- precedence rule of the logical/arithmetic expressions

- REPL

- REPL: undisplay previous session results: have a variable in the interpreter that controls where the stdout can be redirected (redirect_stream parameter, by default sys.__stdout__)

- [X] REPL: Error recovery: if error occurs, do NOT append the current line, and recovery to the previous unerrored state. Present error message

- [X] unary expression

Add External arguments in the signal that gets added to the context when evaluating

Add array data type to STL script

make sure when evaluating to a list, compare every single one of them


in the future, maybe make array a type, and [1, 2, 3] > 1 as a syntactic sugar -
then add support for meta variable evaluation

Add array structure requires changes for parser compoenent for all the STL formula