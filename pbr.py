import re
from copy import deepcopy as dc #take that immutables!

def dpll(clauses, atoms):
    # this is going to be butchered so don't modify the original data
    c = dc(clauses)

    if c == []: return True # c is sat
    elif [] in c: return False # c contains an empty clause
    
    for a in atoms:
        unit_prop(a, c)

    # return dpll(clauses + [a], atoms) or dpll(clauses + ['!'+a], atoms)

def unit_prop(atom, clauses):
    # value for the negated atom
    if '!' in atom:
        neg = atom.replace('!', '')
    else:
        neg = '!' + atom

    # for every clause, delete it if it is true, delete contradictions
    i = 0
    while i < len(clauses):
        j = 0
        while j < len(clauses):
            if clauses[i][j] == atom:
                del clauses[i]
                i -= 1
                break
            elif clauses[i][j] == neg:
                del clauses[i][j]
            else: j += 1

        i += 1
