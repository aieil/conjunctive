import logicparse as lp
from neg import neg, invert

def elim(formula):
    # combined elimination of <-> and ->
    iffIndices = findall(formula, '<->')
    if iffIndices != []: #eliminate top level iffs
        lastIffIndex = iffIndices[-1]
        termA = elim(formula[:lastIffIndex])     # start of list to <->
        termB = elim(formula[lastIffIndex + 1:]) # <-> to end of list.
        #formula = [[termA, '->', termB], '^', [termB, '->', termA]]
        formula = [['!',termA, 'v', termB], '^',['!',termB, 'v', termA]]
    else: # eliminate implications
        impIndices = findall(formula, '->')
        if impIndices != []:
            lastImpIndex = impIndices[-1]
            termA = elim(formula[:lastImpIndex])
            termB = elim(formula[lastImpIndex + 1:])
<<<<<<< Updated upstream
            formula = ['!', termA, 'v', termB]
=======
            formula = []
>>>>>>> Stashed changes
    return formula

# def collapse_not(expr_list):
#     """
#     Takes a nested expression tree thing, checks for uncollapsed nots
#     """
#     for each in expr_list:


# def demorgan(formula): return neg([invert(symbol) if symbol in ('^', 'v') else neg(symbol) for symbol in formula])

def demorgan(formula):
    output = []
    for symbol in formula:

        if symbol in ('^', 'v'):

            output.append(invert(symbol))
        else:

            output.append(neg(symbol))

    return neg(output)


def findall(seq, elem):
    """
    find indices of all occurences of elem at top level of list.
    """
    return [i for i in range(0, len(seq)) if seq[i] == elem]
