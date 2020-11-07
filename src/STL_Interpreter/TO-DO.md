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



Task for Saturday, 10/7/2020
- Boolean Logical expressions (both unary and binary)
- signal evaluation using STL formulas
        - standardize signal formats
        - evaluation functions for different STL formulas
- type check (type context)
- val and var declaration (don't allow redeclaration?)
- evaluation of variable formulas (eval context)
- create type for each primitive values (as separate classes)

- limit the update of the context according to the 
        - val decl
        - type tags!

- do not allow re-assignment for val declaration
        - implement var declaration first

- block statement?