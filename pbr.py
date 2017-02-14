import re
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
    if c == [] or all(len(clause) == 1 for clauses in c): return True
    elif [] in c: return False # c contains an empty clause

    for literal in units(clauses):
        unit_prop(literal, c, l)
    pure_lit(l, c)

    # take the 1st available literal
    return dpll(c+[l[0]], l) or dpll(c+[neg(l[0])], l)

# performs both unit propagation and pure literal functions
def unit_prop(literal, clauses):
    n = neg(literal)

    # eliminate literal from literals
    i = 0
    while i < len(literals):
        if literals[i] == n or literals[i] == literal:
            del literals[i]
        else:
            i += 1

    # given literal:
    # for every clause, delete it if it is true, delete contradictions
    i = 0
    while i < len(clauses):
        j = 0
        while j < len(clauses[i]):
            if clauses[i][j] == literal:
                del clauses[i]
                i -= 1
                break
            elif clauses[i][j] == n:
                del clauses[i][j]
            else: j += 1

        i += 1

# deletes all pure literals
def pure_lit(clauses, literals):
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
    
# returns list of literals that appear as unit clauses
def units(clauses): return [c[0] for c in clauses if len(c) == 1]

# returns the negative of a literal
# e.g. given Cat returns !Cat, vice-versa
def neg(literal): return literal[1:] if literal[0] == '!' else '!' + literal
