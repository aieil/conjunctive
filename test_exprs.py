e1 = "A<->!B<->C^DvX->Z"
e2 = "((!meow->moo)vWoof)<->squeek->chinchilla"
e3 = "(!AvB)"
e4 = "!(A^(Bv!C))"
e5 = "!Av(D^B)"
e6 = "!A->(Bv!C)"
e7 = "!!A<->!B<->!!C^DvX->Z"
e8 = "!!A<->(!B)<->!(!C)^DvX->Z"
e9 = "!(!(!(MEOW)))"
e10 = "((((atom))))"

l1 = ["!", ["A", 'v', 'B']]

doublenot = ['!', ['!', ['A', '^', 'B']]]

singletons = ['!',
 [['!',
   [['!',
     [['!', [[['!', ['!A']], 'v', ['B']], '^', [['!', ['B']], 'v', ['!A']]]]]],
    'v',
    [['!', [['!', [['!', [['C', '^', 'D'], 'v', 'X']]]], 'v', 'Z']]]]],
  'v',
  ['!',
   [['!', [['!', [['!', [['!', [['C', '^', 'D'], 'v', 'X']]]], 'v', 'Z']]]],
    'v',
    [['!', [[['!', ['!A']], 'v', ['B']], '^', [['!', ['B']], 'v', ['!A']]]]]]]]]

expressions = [e1, e2, e3, e4, e5]
