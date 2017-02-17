import logicparse as lp
import copy
from neg import neg, invert


def convert(formula):
    # step 1 remove <->, ->
    # step 2 move negation inwards.
    # step 3
    # step 4
    pass


def elim(formula):
    # combined elimination of <-> and ->
    formula = copy.deepcopy(formula)
    iffIndices = findall(formula, '<->')
    if iffIndices != []: #eliminate top level iffs
        lastIffIndex = iffIndices[-1]
        termA = elim(formula[:lastIffIndex])     # start of list to <->
        flatten_singletons(termA)
        termB = elim(formula[lastIffIndex + 1:]) # <-> to end of list.
        flatten_singletons(termB)
        #formula = [[termA, '->', termB], '^', [termB, '->', termA]]
        #formula = [['!',termA, 'v', termB], '^',['!',termB, 'v', termA]]
        formula = [[demorgan_c(termA), 'v', termB], '^',[demorgan_c(termB), 'v', termA]]
    elif findall(formula, '->') != []:
        impIndices = findall(formula, '->')
        if impIndices != []:
            lastImpIndex = impIndices[-1]
            termA = elim(formula[:lastImpIndex])
            termB = elim(formula[lastImpIndex + 1:])
            #formula = ['!', termA, 'v', termB]
            formula = [demorgan_c(termA), 'v', termB]
    else:
        # otherwise, if there are no implications at the top level,
        # loop through any bracketed expressions and eliminate any nested imps.
        for i in range(len(formula)):
            if type(formula[i]) is list:
                formula[i] = elim(formula[i])

    flatten_singletons(formula)

    return formula

# def collapse_not(expr_list):
#     """
#     Takes a nested expression tree thing, checks for uncollapsed nots
#     """
#     for each in expr_list:

def distribute_or(formula):
    formula = copy.deepcopy(formula)
    output = []
    for i in range(len(formula)):
        if type(formula[i]) is list:
             output.append(distribute_or(formula[i]))
        elif formula[i] == 'v' and  type(formula[i+1]) is list:
            # remove the next item from the formula list, and call distribute
            # on it.
            # remove last element and set to previous symbol.
            prevSymbol = output.pop() # this will already be distributed.
            # lis.pop(i) I have no idea what this would be for.
            brackSymbol = distribute_or(formula.pop(i+1))

            newExpression = []
            for j in range(len(brackSymbol)):
                if brackSymbol[j] != '^': # note: there shouldn't be ors.
                    newExpression += [[prevSymbol, 'v', brackSymbol[j]], '^']


            newExpression.pop() # have to remove a trailing ^
        #else:
            # formula[i] is a string. Only thing is if it is a !.
            # demorgans will have been recursively applied beforehand, so it
            # won't happen.


"""
May need to to recursively apply demorgans, to it's own result,
"""


def flatten_singletons(lis):
    # finds lists containing a single item and moves that item up to the top level. Not recursive or anything. Only top level.
    for i in range(len(lis)):
        if type(lis[i]) is list and len(lis[i]) == 1:
            lis[i] = lis[i][0]


"""
function to flatten a nested list found at:
http://rightfootin.blogspot.ca/2006/09/more-on-python-flatten.html
I can't take credit.
"""

def iter_flatten(iterable):
    it = iter(iterable)
    for e in it:
        if isinstance(e, (list, tuple)):
            for f in iter_flatten(e):
                yield f
        else:
            yield e


# The c is for correct because this version actually works
# negates the expression and then performs the demorgan operation on its
# contents

# def demorgan(formula): return neg([invert(symbol) if symbol in ('^', 'v') else neg(symbol) for symbol in formula])
def demorgan(formula):
    output = neg(formula)

    if output[0] == '!':
        demorgan_op(output[1])
    else:
        demorgan_op(output)

    return output

# demorgan operation: negates literals and bracketed expressions,
# inverts conjunctions and disjunctions
def demorgan_op(formula):
    for symbol in enumerate(formula):
        if symbol[1] in ('^', 'v'):
            formula[symbol[0]] = invert(symbol[1])
        # probably shouldn't ever happen?
        elif symbol[1] == '!':
            del formula[symbol[0]]
        else:
            formula[symbol[0]] = neg(symbol[1])

# applies demorgan's theorem recursively to resolve negated bracketed
# expressions
def demorgan_r(formula):
    output = demorgan(formula)

    for clause in enumerate(output):
        if type(clause[1]) == list:
            output[clause[0]] = demorgan_r(clause[1])
            print("did step two!")

    return output

def findall(seq, elem):
    """
    find indices of all occurences of elem at top level of list.
    """
    return [i for i in range(0, len(seq)) if seq[i] == elem]
