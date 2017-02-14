import re

# globally defined regex matches brackets, atoms, and operators
r = r'\(|\)|!?[A-Z,a-u,w-z,0-9]+|\<\-\>|\-\>|\^|v|!'
# regex for just the operators
opers = r'\<\-\>|\-\>|\^|v|!'

# separates logical expression into list of values matching r
def parse(expr): return re.findall(r, expr)

# generates a nested list of logical expressions
# destructive, shouldn't be messed with without copying
def nestgen(lis):
    v = []

    while lis:
        curr = lis.pop(0)

        if curr == '(':
            v.append(nestgen(lis))
        elif curr == ')':
            return v
        else:
            v.append(curr)

    return v
