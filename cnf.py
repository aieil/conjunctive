import logicparse as lp
import copy
from neg import neg, invert
import sys
import pprint


def convert(formulaString):
    sys.setrecursionlimit(3000) # yikes

    # using nestgen will not require any changes. It may mean some cases are
    # unused.
    formula = lp.nestgen(lp.parse(formulaString), extend = True)
    pprint.pprint(formula)
    # step 1 remove <->, ->
    formula = elim(formula)
    formula = flatten_singletons_r(formula)
    print("after elimination:")
    pprint.pprint(formula)

    # step 2 move negation inwards. #done.
    formula = jlDemorgan_r(formula)
    print("after demorgans:")
    pprint.pprint(formula)

    # step 3



def elim(formula):
    # combined elimination of <-> and ->
    formula = copy.deepcopy(formula)
    iffIndices = findall(formula, '<->')
    if iffIndices != []: #eliminate top level iffs
        lastIffIndex = iffIndices[-1]
        termA = elim(formula[:lastIffIndex])     # start of list to <->
        #flatten_singletons(termA)
        termB = elim(formula[lastIffIndex + 1:]) # <-> to end of list.
        #flatten_singletons(termB)
        #formula = [[termA, '->', termB], '^', [termB, '->', termA]]
        #formula = [['!',termA, 'v', termB], '^',['!',termB, 'v', termA]]
        formula = [[neg(termA), 'v', termB], '^', [neg(termB), 'v', termA]]
    elif findall(formula, '->') != []:
        impIndices = findall(formula, '->')
        if impIndices != []:
            lastImpIndex = impIndices[-1]
            termA = elim(formula[:lastImpIndex])
            termB = elim(formula[lastImpIndex + 1:])
            #formula = ['!', termA, 'v', termB]
            # if type(termA) is str:
            #     formula = [neg(termA), 'v', termB]
            # else:
            #     formula = [neg(termA), 'v', termB]
            formula = [neg(termA), 'v', termB]
    else:
        # otherwise, if there are no implications at the top level,
        # loop through any bracketed expressions and eliminate any nested imps.
        for i in range(len(formula)):
            if type(formula[i]) is list:
                formula[i] = elim(formula[i])
    #flatten_singletons(formula)

    return formula


def distribute_or(formula):
    """
    at this point, all negation should have been moved inwards and merged with
    atoms. This means that there are 2 possible lengths for formula:

    # is there such thing as empty formulas for this assignment? like ()
    # or a formula that's just ((((atom)))) or something.

    # case a) len = 1: formula is an atom. In this case, formula will be a
    string.

    # case b) len = 3: expression of the form A v B or A ^ B.

    if lower case letters represent atoms, and upper case represents a compound
    expression: the possible structures for a formula of length 3 (case b) are:
    case 1 a v b -> return # base case!
    case 2 a ^ b -> return # base case
    case 3 a v B -> distribute
    case 4 a ^ B -> recur on B
    case 5 B v a -> a v B
    case 6 B ^ a -> a ^ B
    case 7 A v B -> distribute -> next condition
    case 8 A ^ B -> recur on A, recur on B

    all of the ^ cases can merge.
    case 1 a v b -> return # base case!
    case 2 a v B -> subcases.
    case 3 A v b -> b v A -> case 2
    case 4 A v B -> subcases
    #### case 5 A ^ B -> recur on A, recur on B ####

    the distribution cases break down into sub cases.


    A v (B v C)
    A v (B ^ C)

    case 2-1 a v (B v C) -> a v recur(B) v recur(C)
    case 2-2 a v (B ^ C) -> recur(a v B) ^ recur(a v C)

    where o is either operation
    case 4-1 (A1 o A2) v (B1 ^ B2) ->
        recur((A1 o A2)vB1)^recur((A1 o A2)vB2)
    case 4-2 (A1 ^ A2) v (B1 v B2) ->
        (B1 v B2) v (A1 ^ A2) -> case 4-1
    case 4-3 (A1 v A2) v (B1 v B2) -> case 5



    """
    ######### case a #########
    if isAtom(formula):
        return formula

    ######### case b #########
    A = formula[0]
    op = formula[1]
    B = formula[2]

    ## case 1
    if isAtom(A) and isAtom(B):
        return formula

    ## case 3
    if isAtom(B): # -- implies A is not an atom.
        A, B = B, A # switch them around!
        # case 3 is now case 2









def isAtom(formula):
    if type(formula) is str:
        return True
    else:
        return False



#
# def distribute_or(formula):
#     formula = copy.deepcopy(formula)
#     output = []
#     for i in range(len(formula)):
#         if type(formula[i]) is list: # see if this element is an atom or a subformula.
#             output.append(distribute_or(formula[i]))
#         elif formula[i] == 'v' and  type(formula[i+1]) is list:
#             # remove the next item from the formula list, and call distribute
#             # on it.
#             # remove last element and set to previous symbol.
#             prevSymbol = output.pop() # this will already be distributed.
#             # lis.pop(i) I have no idea what this would be for.
#             brackSymbol = distribute_or(formula.pop(i+1))
#
#             newExpression = []
#             for j in range(len(brackSymbol)):
#                 if brackSymbol[j] != '^': # note: there shouldn't be ors.
#                     newExpression += [[prevSymbol, 'v', brackSymbol[j]], '^']
#
#
#             newExpression.pop() # have to remove a trailing ^
#         #else:
#             # formula[i] is a string. Only thing is if it is a !.
#             # demorgans will have been recursively applied beforehand, so it
#             # won't happen.

# def distribute_or2(formula):
#
#     # base case of the recursion: this is an atom. return it unchanged.
#     if type(formula) is not list:
#         return formula
#     # else, it is a list representing a binary operator and 2 operands.
#     # must have length 3.
#     # it could still be a singleton list.
#     # This entire thing will already be in precidence nested groups.
#     formula = deepcopy(formula)
#     output = []
#
#     if len(formula) == 1:
#         # just check whether singleton lists will happen.
#         print("found a singleton list!!")
#         # if there are singleton lists, the solution is to both flatten
#         # and call recursively.
#         return distribute_or2(formula[0])
#
#
#     # case 1: 2 elements joined by ^
#     # in this case recur on each.
#     if formula[1] == '^':
#         A = formula[0]
#         B = formula[2]
#         output.append(distribute_or2(A))
#         output.append('^')
#         output.append(distribute_or2(B))
#         return output

    # case 2: 2 elements joined by v
    # transform, then call recusively on each new term.
    #if formula[1] == 'v':

    # I think that's how this would work. This is NOT very efficient. Gross.
    # too much recursion.


# def distribute_element(A, BandC):
#     # take an element Av(B^C) and do the distribution operation.
#     if len(BandC) == 1:
#         # singleton list. flattens to [AvBandC[0]]
#         # could be a singleton nested list [[aardvark]].
#         # negation should be at the bottom level.
#         return [A, 'v', BandC]
#     elif len(BandC) == 3:
#         return [[A, 'v', BandC[0]], '^', [A, 'v', BandC[2]]]



def flatten_singletons(lis):
    # finds lists containing a single item and moves that item up to the top level. Not recursive or anything. Only top level.
    for i in range(len(lis)):
        if type(lis[i]) is list and len(lis[i]) == 1:
            lis[i] = lis[i][0]


def flatten_singletons_r(lis):
    # recursively go through a list and flatten singletons.
    # base case 1
    if type(lis) is not list:
        return lis

    elif len(lis) == 1 and type(lis) is list:
        return flatten_singletons_r(lis[0])
    else:
        output = []
        flatten_singletons(lis)
        for each in lis:
            # note:
            # [] += 'meow' -> ['m', 'e', 'o', 'w']
            if type(each) is not list:
                output.append(each)
            elif type(each) is list:
                output.append(flatten_singletons_r(each))
        return output


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
# def demorgan(formula):
#     output = neg(formula)
#     if output[0] == '!':
#         demorgan_op(output[1])
#     else:
#         demorgan_op(output)
#
#     return output

# demorgan operation: negates literals and bracketed expressions,
# inverts conjunctions and disjunctions
# def demorgan_op(formula):
#     for symbol in enumerate(formula):
#         if symbol[1] in ('^', 'v'):
#             formula[symbol[0]] = invert(symbol[1])
#         # probably shouldn't ever happen?
#         elif symbol[1] == '!':
#             del formula[symbol[0]]
#         else:
#             formula[symbol[0]] = neg(symbol[1])
#     # JL added
#     return formula
#     # end JL added

# applies demorgan's theorem recursively to resolve negated bracketed
# expressions
# def demorgan_r(formula):
#     output = demorgan(formula)
#     #print(output)
#     i = 0
#     while i < len(output):
#         #print(output[i])
#         if type(output[i]) == list and output[i][0] == '!':
#             output[i] = demorgan_r(output[i])
#
#         i += 1
#
#     return output

def jlDemorgan_r(formula):
    print("length of formula = ", len(formula))
    # output will be unchanged if length is not 2
    output = jlDemorgan(formula)
    # output should now be of the form AvB or else simply an atom
    for i in range(len(output)):
        if type(output[i]) is list:
            output[i] = jlDemorgan_r(output[i])
    return output

def jlDemorgan(formula):
    """
    Takes a formula. Will demorgan it, if and only if
    it is a list of length 2. Expressions without a ! at the top level will
    not be demorganed.
    """
    if type(formula) is not list:
        print("JLdemorgans called with non-list argument.")
        return formula
    elif len(formula) == 2:
        # the only case in which demorgans should be applied is if there is a
        # negated inner list, with an or or and.
        # [!, [meowA ^ meowB]] -> [!meowA v !meowB]
        if len(formula[1]) == 3:
            A = formula[1][0]
            operator = formula[1][1]
            B = formula[1][2]
            return [neg(A), invert(operator), neg(B)]
        else:
            # f[1] = [! [blah]]
            # [blah] # assume no singletons.
            return neg(formula[1]) # eliminate not.
    else: # in this case, it's a normal binary expression. Leave it unchanged.
        return formula

def collapse_double_negation(formula):
    # check for invalid input
    if type(formula) is not list:
        print("collapse double negation called with string argument not list")
        return formula
    elif len(formula) == 2 and len(formula[1]) == 2:
        return formula[1][1]
    else:
        return formula


def findall(seq, elem):
    """
    find indices of all occurences of elem at top level of list.
    """
    return [i for i in range(0, len(seq)) if seq[i] == elem]
