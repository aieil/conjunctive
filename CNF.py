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

    # preprocessing:
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
        # give this inner function access to rebind the variables
        # in the outer function.
        nonlocal ptr
        nonlocal ptr2
        ptr += 1
        # 3 conditions:
        # a single variable:
        if formula[ptr2].isalpha():
            return '!' + formula[ptr];
        elif formula[ptr] == '!':
            # recursively add the sequence of nots.
            return '!' + lookAheadNot()

    # def lookAheadParen():
    #     nonlocal ptr
    #     #nonlocal ptr2
    #     parenChunk = "("
    #     nOpen = 1 # tracks the number of open parentheses.
    #     while(nOpen > 0): # eat characters until the parens are matched
    #         ptr += 1
    #         char = formula[ptr]
    #         if char == '(':
    #             nOpen = nOpen + 1
    #         elif char == ')':
    #             nOpen = nOpen - 1
    #
    #         parenChunk = parenChunk + char
    #
    #     return parenChunk

    while ptr < S:
        # different cases:
        if formula[ptr] == '!':
            chunks.append(lookAheadNot())
            ptr = ptr2

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
            while formula[ptr].isalpha():
                var += formula[ptr]
                ptr += 1
            chunks.append(var)
        ptr += 1
        print(chunks)
    return chunks
