import re

# globally defined regex matches brackets, atoms, and operators
splitter = r'\(|\)|!?[A-Za-uw-z0-9]+|\<\-\>|\-\>|\^|v|!'

# separates logical expression into list of values matching r
def parse(expr): 
    return re.findall(splitter, expr)

# generates a nested list of logical expressions
# destructive, shouldn't be messed with without copying
def nestgen(lis, extend=False):
    nested_expr = []
    # precedence (), !, ^, v, ->, <->

    # parentheses
    while lis:
        curr = lis.pop(0)

        if curr == '(':
            nested_expr.append(nestgen(lis))
        elif curr == ')':
            return nested_expr
        else:
            nested_expr.append(curr)

    if extend:
        for e in enumerate(nested_expr):
            if type(e[1]) == list:
                nested_expr[e[0]] = nestgen(nested_expr[e[0]])

        # negation
        find_and_group(nested_expr, '!', 2)

        # conjunction
        find_and_group(nested_expr, '^')

        # disjunction
        find_and_group(nested_expr, 'v')

        # implication
        find_and_group(nested_expr, '->')

        # iff
        find_and_group(nested_expr, '<->')

    return nested_expr

# finds logic operators of given type, groups values around it in a 
# bracketed expression
def find_and_group(lis, oper, groupsize=3):
    i = 0
    while len(lis) > groupsize and i < len(lis) - (groupsize - 1):
        if lis[i + (groupsize - 2)] == oper:
            lis[i] = [lis[j] for j in range(i, i+groupsize)]
            for j in range(groupsize-1): del lis[i+1]
        i += 1

# for the three-colour problem, just goes through the list and 
# makes the strings into integers
def make_ints(lis):
    return [int(e) if type(e) == str else make_ints(e) if type(e) == list \
            else e for e in lis]
