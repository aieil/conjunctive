# pbr
# performs a proof by refutation using an implementation of the dpll 
# algorithm
# 
from copy import deepcopy as dc #take that mutables!

# returns true if SAT
def pbr(clauses):
    # make a list of literals
    literals = []
    for clause in clauses:
        for literal in clause:
            if literal not in literals:
                literals.append(literal)

    # run dpll
    return dpll(clauses, literals)

# implementation of dpll, preprocessing for some complexity gains
def dpll(clauses, literals):
    # these are going to be butchered so don't modify the original data
    c = dc(clauses)
    l = dc(literals)
 
    # c contains only unit clauses or is empty
    if c == [] or all(len(clause) == 1 for clause in c): return True
    elif [] in c: return False # c contains an empty clause

    # unit propagation
    for literal in units(clauses):
        unit_prop(literal, c, l)

    # pure literal step
    pure_lit(l, c)
    
    # take the 1st available literal
    if l:
        return dpll(c+[l[0]], l) or dpll(c+[neg(l[0])], l)
    # if there aren't any we are done, recurse once more for solution
    return dpll(c, l)

# performs both unit propagation and pure literal functions
def unit_prop(literal, clauses, literals):
    n = neg(literal)

    clear(n, literals) # n is about to be eliminated

    # given literal:
    # for every clause, delete it if it is true, delete contradictions
    i = 0
    while i < len(clauses):
        j = 0
        while j < len(clauses[i]):
            if clauses[i][j] == literal:
                for l in clauses[i][j]:
                    clear(l, literals)
                del clauses[i]
                i -= 1
                break
            elif clauses[i][j] == n:
                del clauses[i][j]
            else: j += 1

        i += 1

# deletes all pure literals
def pure_lit(literals, clauses):
    i = 0
    
    while i < len(literals):
        if neg(literals[i]) not in literals:
            j = 0
            while j < len(clauses):
                if literals[i] in clauses[j]:
                    del clauses[j]
                else:
                    j += 1
            del literals[i]
        else:
            i += 1

# removes element from list
# I thought this would be more useful than it turned out to be
def clear(el, ls, single=True):
    i = 0
    while i < len(ls):
        if ls[i] == el:
            del ls[i]
            if single: return
        else:
            i += 1
    
# returns list of literals that appear as unit clauses
def units(clauses): return [c[0] for c in clauses if len(c) == 1]

# returns the negative of a literal
# e.g. given Cat returns !Cat, vice-versa
def neg(literal): return literal[1:] if literal[0] == '!' else '!' + literal
