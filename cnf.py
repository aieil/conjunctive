import logicparse as lp
import copy
from neg import neg, invert
import sys
import pprint


def convert(formula):
    sys.setrecursionlimit(4000)
    formula = copy.deepcopy(formula)

    formula = elim(formula)
    formula = flatten_singletons_r(formula)
    # print("after elimination:")
    # pprint.pprint(formula)

    # step 2 move negation inwards, eliminate double negation. #done.
    formula = jlDemorgan_r(formula)
    # print("after demorgans:")
    # pprint.pprint(formula)

    # step 3
    # print("distributed formula")
    formula = distribute_or(formula)
    # pprint.pprint(formula)


    if not isAtom(formula):
        flattened = list(iter_flatten(formula))
        # print(flattened)
    else:
        flattened = [formula]
    # now have to make this into sequences of cnf terms.
    #andindices = findall(flattened, '^')

    # print("clause form:")
    cf =  splitlist(flattened, '^')
    # print(cf)

    delete_or(cf)

    #eliminate tautologies.

    return cf





def convert_test(formulaString):
    sys.setrecursionlimit(3000) # yikes

    # using nestgen will not require any changes. It may mean some cases are
    # unused.
    formula = lp.nestgen(lp.parse(formulaString), extend = True)
    pprint.pprint(formula)
    # step 1 remove <->, ->
    formula = elim(formula)
    formula = flatten_singletons_r(formula)
    # print("after elimination:")
    # pprint.pprint(formula)

    # step 2 move negation inwards, eliminate double negation. #done.
    formula = jlDemorgan_r(formula)
    # print("after demorgans:")
    # pprint.pprint(formula)

    # step 3
    # print("distributed formula")
    formula = distribute_or(formula)
    # pprint.pprint(formula)


    if not isAtom(formula):
        flattened = list(iter_flatten(formula))
        # print(flattened)
    else:
        flattened = [formula]
    # now have to make this into sequences of cnf terms.
    #andindices = findall(flattened, '^')

    # print("clause form:")
    cf =  splitlist(flattened, '^')
    # print(cf)

    delete_or(cf)

    # print("clause form:")
    cf =  splitlist(flattened, '^')
    # print(cf)

    delete_or(cf)



    return cf

def correct_tautology(terms):
    newlist = []
    for each in terms:
        if neg(each) not in terms:
            newlist.append(each)
    terms = newlist
    # unfortuneately this means that the list will now contain some empty lists.

def elim(formula):
    # combined elimination of <-> and ->
    formula = copy.deepcopy(formula)
    iffIndices = findall(formula, '<->')
    if iffIndices != []: #eliminate top level iffs
        lastIffIndex = iffIndices[-1]
        termA = elim(formula[:lastIffIndex])     # start of list to <->
        termB = elim(formula[lastIffIndex + 1:]) # <-> to end of list.

        formula = [[neg(termA), 'v', termB], '^', [neg(termB), 'v', termA]]
    elif findall(formula, '->') != []:
        impIndices = findall(formula, '->')
        if impIndices != []:
            lastImpIndex = impIndices[-1]
            termA = elim(formula[:lastImpIndex])
            termB = elim(formula[lastImpIndex + 1:])

            formula = [neg(termA), 'v', termB]
    else:
        # otherwise, if there are no implications at the top level,
        # loop through any bracketed expressions and eliminate any nested imps.
        for i in range(len(formula)):
            if type(formula[i]) is list:
                formula[i] = elim(formula[i])

    return formula


def delete_or(clauses):
    #print("deleting or:")
    for clause in clauses:
        #print(clause)
        orinds = findall(clause, 'v')
        #print(orinds)
        if orinds != []:
            i = 0
            while i < len(orinds):
                # have to reduce the index, to account for indices already
                # deleted.
                del clause[orinds[i] - i]
                i += 1


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
    # print("distribute or on formula:")
    # print(formula)

    if isAtom(formula):
        return formula

    ######### case b #########
    A = formula[0]
    op = formula[1]
    B = formula[2]

    ## case 1 ## base case.
    if isAtom(A) and isAtom(B):
        return formula

    ## case 5 ##
    if op == '^':
        return [distribute_or(A), '^', distribute_or(B)]
    # done case 5.

    # implies operator

    ## case 3 ##
    if not isAtom(A) and isAtom(B):
        A, B = B, A # switch them around!
        # case 3 is now case 2
        # can just reconstruct the formula and call the function recursively again.
        # otherwise, probably better to just fall down to case 2.
        # for the time being, former solution.
        return distribute_or([A, 'v', B]) # will now go to case 2.

    # a is atom but b is not:
    if isAtom(A):
        B1 = B[0]
        Bop = B[1]
        B2 = B[2]
        if Bop == '^':
            return [distribute_or([A, 'v', B1]), '^',
                distribute_or([A, 'v', B2])]
        else:
            return [A, 'v', distribute_or(B)]

    else:
        return distrib_doublecase(A,B)





def distrib_doublecase(A, B):
    # A v B
    # A v (B1 ^ B2)
    B1 = B[0]

    Bop = B[1]

    B2 = B[2]


    A1 = A[0]
    Aop = A[1]
    A2 = A[2]

    if Bop == '^':
        return [distribute_or([A,'v',B1]), '^', distribute_or([A, 'v', B2])]
    elif Aop == '^': # and Bop == v
        return [distribute_or([B, 'v', A1]), '^', distribute_or([B, 'v', A2])]
    else: # Aop, Bop = v
        return [[distribute_or(A1), 'v', distribute_or(A2)], '^',
                        [distribute_or(B1), 'v', distribute_or(B2)]]



def isAtom(formula):
    if type(formula) is str:
        return True
    else:
        return False



def flatten_singletons(lis):
    # finds lists containing a single item and moves that item up to the top level. Not recursive or anything. Only top level.
    for i in range(len(lis)):
        if type(lis[i]) is list and len(lis[i]) == 1:
            lis[i] = lis[i][0]


def flatten_singletons_r(lis):
    # recursively go through a list and flatten singletons.

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



def jlDemorgan_r(formula):
    # output will be unchanged if length is not 2
    output = jlDemorgan(formula)
    # output should now be of the form AvB or else simply an atom
    if type(output) is str:
        return output
    if len(output) == 2 and type(output) is list:
        return jlDemorgan_r(output)
    for i in range(len(output)):
        if type(output[i]) is list:
            output[i] = jlDemorgan_r(output[i])
    #print("demorgan output of formula:", formula)
    #print(output)
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
        if type(formula[1]) is list and len(formula[1]) == 3:
            A = formula[1][0]
            operator = formula[1][1]
            B = formula[1][2]
            return [neg(A), invert(operator), neg(B)]
        else:
            # f[1] = [! [blah]]
            # [blah] # assume no singletons.
            # [! blah]
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


def splitlist(jlist, elem):
    if elem not in jlist:
        return [jlist] # return the list wrapped in another list.
    split = []
    i = 0
    sublist = []
    while i < len(jlist):
        if not jlist[i] == elem:
            sublist.append(jlist[i])
        else:
            split.append(sublist)
            sublist = []
        i += 1
    split.append(sublist)

    return split



def findall(seq, elem):
    """
    find indices of all occurences of elem at top level of list.
    """
    return [i for i in range(0, len(seq)) if seq[i] == elem]
