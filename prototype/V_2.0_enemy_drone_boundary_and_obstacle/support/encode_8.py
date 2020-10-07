# encode_8.py
# Thu Sep 24 16:45:08 EDT 2020

# https://stackoverflow.com/questions/594266/equation-parsing-in-python
#   (https://en.wikipedia.org/wiki/Lemniscate) the length of the map

import parser
import math

formula_1 = "math.sqrt(-x**4 + x**2)" # y > 0
formula_2 = "-math.sqrt(-x**4 + x**2)" # y < 0

formula_1_parsed = parser.expr(formula_1).compile()
formula_2_parsed = parser.expr(formula_2).compile()
x = 0.8
print(eval(formula_1))

# use this approach to find the closest discretized point.