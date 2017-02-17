# main module
# runs problem solutions
from sys import argv
import cnf
import pbr
import logicparse as lp

usage = """
usage: as3 <option> <source> [output]

    [output] is a local file name, it will be created if it does not exist
    or overwritten if it does. If no file is specified, results will be
    written to stdout

    -h      show help
    
    -c      interpret <source> as a logical expression and write CNF clause
            form to [output]

    -p      interpret <source> as a series of logical expressions and
            use proof-by-refutation to determine whether it is satisfiable,
            writes result to [output]

    -t      interpret <source> as a set of edges, determine if there is a 
            solution to the three-colour problem for that graph, writes the 
            result to [output]
"""

def main():
    if argv[1] == '-c':
        #cnf here
        pass
    elif argv[1] == '-p':
        #pbr here
        pass
    elif argv[1] == '-t':
        pass
    else:
        print(usage)


if __name__ == "__main__":
    main()
