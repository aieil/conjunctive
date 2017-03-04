import re
from neg import neg

# globally defined regex matches brackets, atoms, and operators
splitter = r'\(|\)|!?[A-Za-uw-z0-9]+|\<\-\>|\-\>|\^|v|!'

# separates logical expression into list of values matching r
def parse(expr):
    return re.findall(splitter, expr)

# parse a multiline expression, negate the conclusion for use with pbr
def parse_multiline(expr):
    parsed_expr = []

    for line in expr.splitlines():
        if 'Therefore' in line:
            parsed_expr += ['^', neg(parse(line)[1:])]
        else:
            parsed_expr += ['^', parse(line)]

    del parsed_expr[0] # delete the first ^, we don't need it
    return parsed_expr

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
        else: i += 1

# convert edge set to matrix
def edges_to_matrix(expr):
    vertices = {}

    # get list of edges by vertex
    for edge in expr:
        if edge[0] not in vertices:
            vertices[edge[0]] = [edge[1]]
        else:
            vertices[edge[0]].append(edge[1])

        if edge[1] not in vertices:
            vertices[edge[1]] = [edge[0]]
        else:
            vertices[edge[1]].append(edge[0])

    # generate n*n matrix
    mat = [[0 for edges in vertices] for edges in vertices]

    # used to index matrix
    vertices_list = sorted(vertices)
    i = 0

    # traverse list of vertices
    while i < len(vertices_list):
        j = 0
        # traverse the list assigned to the current vertex
        while j < len(vertices[vertices_list[i]]):
            # get the corresponding index of the connecting node k
            # set mat[i][k] = 1
            mat[i][vertices_list.index(vertices[vertices_list[i]][j])] = 1
            j += 1
        i += 1

    return mat, vertices_list
