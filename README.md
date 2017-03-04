# conjunctive
* __converts logical expressions to CNF__
* __performs proofs-by-refutation__
* __solves the three-colour problem__

## use
    python as2.py <option> <source> [output]

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

Code designed for Python 3.x. If you try to use Python 2.x, you will get errors.
