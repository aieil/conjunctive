import re


"""
Convert to conjunctive normal form.
"""
# cnf :: String -> [(String, String)]
def cnf(formula):
    """
    Given an input formula, computes equivalent cnf statement
    """
    symbols = "()!<>-^v"

    #preparation:
    formula = formula.strip().replace(" ", "") #remove spaces.
    # to make it easier, replace -> and <-> with single character
    # standins.
    # how about:
    #---------- <-> = % ------------
    #---------- -> = $
    formula = formula.replace("<->", '%')
    formula = formula.replace("->", '$')

    #divide this up into operator precedence.
    #chunks = [] #a chunk will group by ! and (), but not by &,|,<->,->
    # step 1: eliminate <->
    # step 2: eliminate ->
    # step 3: eliminate move ! inwards. !!x, !(x^y)
    # step 4: distribute v: x v (y ^ z)

    # ok, to parse this, I'm going to step through character by character.


def chunk(formula):
    S = len(formula)
    chunks = []
    ptr = 0
    ptr2 = 0
    def lookAheadNot():
        ptr2 = ptr + 1
        # 3 conditions:
        # a single variable:
        if formula[ptr2].isAlpha():
            return '!' + formula[ptr2];
        # a !
        elif formula[ptr2] == '!':
            #oldPtr = ptr
            # use the new position as starting point for next call
            ptr = ptr2
            return '!' + lookAheadNot()

    while ptr < len(formula):
        # different cases:
        # (
        # !
        # )
        if formula[ptr] == '!':
            chunks.append(lookAheadNot())
            ptr = ptr2
        else:
            chunks.append(formula[ptr])
