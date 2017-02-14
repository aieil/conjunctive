import re


"""
Convert to conjunctive normal form.
"""
# cnf :: String -> [(String, String)]
def cnf(formula):
    """
    Given an input formula, computes equivalent cnf statement
    """
    # divide this up into operator precedence.
    # step 1: eliminate <->
    # step 2: eliminate ->
    # step 3: eliminate move ! inwards. !!x, !(x^y)
    # step 4: distribute v: x v (y ^ z)
    # ok, to parse this, I'm going to step through character by character.
    pass


def preprocess(formula):
    # preprocessing:
    formula = formula.strip().replace(" ", "") #remove spaces.
    # to make it easier, replace -> and <-> with single character
    # standins.
    # how about:
    #---------- <-> = % ------------
    #---------- -> = $
    formula = formula.replace("<->", '%')
    formula = formula.replace("->", '$')
    formula = formula.replace("v", "|")
    formula = formula.replace("^", "&")
    return formula


def chunk(formula):
    S = len(formula)
    chunks = []
    ptr = 0
    def lookAheadNot():
        # give this inner function access to ptr in the outer function.
        nonlocal ptr
        ptr += 1
        # 3 conditions:
        # a single variable:
        if formula[ptr].isalpha(): # this case needs to get the whole variable.
            return '!' + formula[ptr];
        elif formula[ptr] == '(':
            return '!' + lookAheadParen()
        elif formula[ptr] == '!':
            # recursively add the sequence of nots.
            return '!' + lookAheadNot()

    def lookAheadParen():
        nonlocal ptr
        parenChunk = "("
        nOpen = 1 # tracks the number of open parentheses.
        while(nOpen > 0): # eat characters until the parens are matched
            ptr += 1
            char = formula[ptr]
            if char == '(':
                nOpen = nOpen + 1
            elif char == ')':
                nOpen = nOpen - 1

            parenChunk = parenChunk + char

        return parenChunk

    while ptr < S:
        # different cases:
        if formula[ptr] == '!':
            chunks.append(lookAheadNot())
            # ptr = ptr2
        elif formula[ptr] == '(':
            parenChunk = "("
            nOpen = 1 # tracks the number of open parentheses.
            while(nOpen > 0): # eat characters until the parens are matched
                ptr += 1
                char = formula[ptr]
                if char == '(':
                    nOpen = nOpen + 1
                elif char == ')':
                    nOpen = nOpen - 1

                parenChunk = parenChunk + char
            chunks.append(parenChunk)
        # note: input preprocessed so that <-> = % and -> = '$'
        elif formula[ptr] == '%' or formula[ptr] == '$':
            chunks.append(formula[ptr])
        else:
            #character is alphabetic.
            var = ""
            while formula[ptr].isalpha(): # add characters until non alpha.
                var += formula[ptr]
                ptr += 1
            chunks.append(var)
        ptr += 1
        print(chunks)
    return chunks
