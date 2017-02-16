# returns the negative of a literal or list
# e.g. given Cat returns !Cat, vice-versa
def neg(expr):
    if type(expr) == str
        return expr[1:] if expr[0] == '!' else '!' + expr
    elif type(expr) == list:
        return expr[1] if expr[0] == '!' else ['!', expr]

# given ^, yields v, vice-versa
def invert(oper):
    if oper == '^': return 'v'
    elif oper == 'v': return '^'
