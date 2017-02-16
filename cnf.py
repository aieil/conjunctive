import logicparse as lp
from neg import neg, invert

def elim(formula):
    # combined elimination of <-> and ->
    iffIndices = findall(formula, '<->')
    if iffIndices != []: #eliminate top level iffs
        # the last one is at the top level since it bind least tightly.
        lastIffIndex = iffIndices[-1]
        termA = elim(formula[:lastIffIndex]) # list up to end.
        termB = elim(formula[lastIffIndex + 1:])
        #formula = [[termA, '->', termB], '^', [termB, '->', termA]]
        formula = [['!',termA, 'v', termB], '^',['!',termB, 'v', termA]]
    else: # eliminate implications
        impIndices = findall(formula, '->')
        if impIndices != []:
            lastImpIndex = impIndices[-1]
            termA = elim(formula[:lastImpIndex])
            termB = elim(formula[lastImpIndex + 1:])
            formula = ['!', termA, 'v', termB]
    return formula

<<<<<<< HEAD
def collapse_not(expr_list):
    """
    Takes a nested expression tree thing, checks for uncollapsed nots
    """

=======
def demorgan(formula):
    return neg([invert(symbol) if symbol in ('^', 'v') else neg(symbol) \
            for symbol in formula])
>>>>>>> master

def findall(seq, elem):
    """
    find indices of all occurences of elem at top level of list.
    """
    return [i for i in range(0, len(seq)) if seq[i] == elem]
