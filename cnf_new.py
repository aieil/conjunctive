import string

class CNFConverter(object):
    """docstring for CNFConvert."""
    def __init__(self):
        self.ptr = 0
        self.chunks = []
        self.variables = set() # record the variables found in formula.

    def convert(self, formula):
        """
        Questions:
        what if it's already in CNF? I don't think that would matter.
        Algorithm should just be able to run through it.
        """
        self.ptr = 0
        self.chunks = [] # reset these.
        formula = preprocess(formula)

    def group_by_iff(self, formula):
        """
        group terms at the top level (treat bracketed stuff as singular) in
        order to shift
        """
        self.ptr = 0 # have to start at the beginning.
        symbols = string.ascii_letters + "!$|&"
        # basically everything that isn't a bracket or an
        # iff can be conglomerated and lumped together.
        # can you have A <-> B <-> C
        # also the case where there is
        terms = []
        term = ""
        while self.ptr < len(formula):
            if formula[self.ptr] == '%':
                # add now ended term to the terms
                terms.append(term)
                term = "" # reset term.
                terms.append('%')
            elif formula[self.ptr] == '(':
                # add bracketed segments as one unit.
                term += self.lookAheadParen(formula)
                # pointer should no be on the last closing bracket.
                # so it's ok to increment ptr.
            elif formula[self.ptr] in symbols:
                term += formula[self.ptr]
            self.ptr += 1
        # this will have had to end on a term or close paren,
        terms.append(term)

    def elim_iff(terms):
        pass

    def lookAheadParen(self, formula):
        """
        progress from the current position to find the matching
        bracket.
        """
        parenChunk = "("
        nOpen = 1 # tracks the number of open parentheses.
        while(nOpen > 0): # eat characters until the parens are matched
            self.ptr += 1
            char = formula[self.ptr]
            if char == '(':
                nOpen = nOpen + 1
            elif char == ')':
                nOpen = nOpen - 1
            parenChunk = parenChunk + char
        return parenChunk

    def lookAheadNot(self, formula):
        self.ptr += 1
        # 3 conditions:
        # a single variable:
        # I'm not bothering with checking for length, because with
        # correct input, string won't end on not.
        if formula[self.ptr].isalpha(): # this case needs to get the whole variable.
            return '!' + formula[self.ptr];
        elif formula[self.ptr] == '(':
            return '!' + self.lookAheadParen()
        elif formula[self.ptr] == '!':
            # recursively add the sequence of nots.
            return '!' + self.lookAheadNot()


    def readVariable(self, formula):
        # assuming pointer is on a letter.
        var = ""
        while self.ptr < len(formula) and formula[self.ptr].isalpha():
            var += formula[self.ptr]
            self.ptr += 1
        self.variables.add(var)
        return var

def preprocess(formula):
    # preprocessing:
    #remove whitespace:
    for each in string.whitespace:
        formula = formula.replace(each, "")
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
