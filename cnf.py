import logicparse as lp

def group_precidence(formulaString):
    formula = lp.nestgen(lp.parse(formulaString))
    # now have to group by operator precidence.
    # am I spelling precidence wrong?
    # <-> binds least tightly.
    # prof seemed to indicate in an example on slack that
    # for A <-> B <-> C or whatever, to group it like
    # (A<->B)<->C

def elim_iff(formula):
    iffIndices = findall(formula, '<->')
    if iffIndices != []:
        # the last one is at the top level since it bind least tightly.
        lastIffIndex = iffIndices[-1]
        termA = elim_iff(formula[:lastIffIndex]) # list up to end.
        print(termA)
        termB = elim_iff(formula[lastIffIndex + 1:])
        # rest of list. Will not contain iff.
        formula = [[termA, '->', termB], '^', [termB, '->', termA]]


    # if neither of these is found, loop through bracketed expressions.
    return formula
    # otherwise: loop through any bracketed expressions.
    # else:
    #     for i in range(len(formula)):
    #         if type(formula[i]) is list:
    #             formula[i] = elim_iff(formula[i])
    #
    # return formula

def elim(formula):
    # combined elimination of <-> and ->
    iffIndices = findall(formula, '<->')
    if iffIndices != []: #eliminate top level iffs
        # the last one is at the top level since it bind least tightly.
        lastIffIndex = iffIndices[-1]
        termA = elim_iff(formula[:lastIffIndex]) # list up to end.
        print(termA)
        termB = elim_iff(formula[lastIffIndex + 1:])
        # rest of list. Will not contain iff.
        formula = [[termA, '->', termB], '^', [termB, '->', termA]]
    else: #eliminate bottom level iffs.
        impIndices = findall(formula, '->')
        if impIndices != []:
            lastImpIndex = impIndices[-1]
            
    return formula



def findall(seq, elem):
    """
    find indices of all occurences of elem at top level of list.
    """
    return [i for i in range(0, len(seq)) if seq[i] == elem]
