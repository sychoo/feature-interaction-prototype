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

- the format of float type must be under scrutiny and its interopeability with Python data type