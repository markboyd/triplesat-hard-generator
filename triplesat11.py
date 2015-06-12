'''
Triplesat.py randomly creates sat formulas with exactly 3 literals per clause, where each clause contains a unique combination of variables
It then evaluates each formula as sat or unsat.
Then it prints stats on the formulas.
Goal: identify the growth of minimally unsatisfiable formulas as n increases
'''

#Known bugs:
#The empty formula returns as unsatisfiable
# "solve_dimacs_formula" has a bug when splitting to the right, do not use 

#This program requires code from https://github.com/nchong/sat
#This code is also found at https://github.com/markboyd/triplesat

from dimacs import solve_dimacs_file, solve_dimacs_formula, is_well_formed
from sat import solve_dpll, solve_dfs, find_unit_clause
import sys
import json


#MerseneTwister pseudo-random hash
from random import *

#pp means "Pretty Print" and trace means "Show the DPLL actions"
pp=False
trace=False

#Break this section of iterating and randomizing formulas out into a function

#Number of iterations and variables
iterations = 10000
numVariables = 6
#testFormulaString = "[[1,-2,4],[-1,2,-5],[1,2,6],[-1,3,-4],[-1,-3,5],[1,3,-6],[-1,4,5],[1,4,-6],[-2,-3,5],[2,-3,-6],[-2,4,-6],[-2,-5,6],[-3,-4,-6]]"
testFormulaString = "[[1,2,-3],[-1,2,4],[-2,3,4],[-1,3,-4],[1,2,-5],[1,3,5],[-2,-3,5],[-2,-4,-5],[-3,4,-5],[-1,2,-6],[-1,-3,6]]"

#Initialize number of unsatisfiable formulas to zero
numunsats = 0
#Initialize the ratio to the float zero
unsatratio = float(0)

if sys.argv[1]:
  print sys.argv[1]
  if sys.argv[1] == "TEST":
    iterations = 2
  else:
    iterations = int(sys.argv[1])

for iter in range (1,iterations):

  #Variables, always start at 1, and up to N variables
  #Set number of clauses to zero for each iteration
  numClauses = 0

  firstvar = 1
  lastvar = numVariables + 1  #Off by one offset error otherwise
    #Create a formula string which is a list of lists (clauses) in JSON
  formulastring="["
  for firstliteral in range (firstvar,lastvar):
    for secondliteral in range (firstliteral+1,lastvar):
        for thirdliteral in range (secondliteral+1,lastvar):
            #for each possible clause, there are 8 combinations of negation
            #one in nine times, the clause should not exist
            if random() < float(1)/9:
                #print "SKIPPED CLAUSE"
                continue
            numClauses += 1
            #for clarity, list all of the signs and randomize
            firsign=""
            secsign=""
            thisign=""
            if random() < 0.5:
                firsign = "-"
            if random() < 0.5:
                secsign = "-"
            if random() < 0.5:
                thisign = "-"
            #assemble the json string
            formulastring+="[%s%s,"%(firsign,firstliteral)
            formulastring+="%s%s,"%(secsign,secondliteral)
            formulastring+="%s%s]"%(thisign,thirdliteral)
            formulastring+=","

  #Be careful, what if there is no clause at all?  Empty formula...
  #This also creates an error because if the random formula is completely empty, it is returned as UNSAT, which convolutes the statistics
  if formulastring.endswith('['):
    #This is an empty formula, so just make it an empty JSON list
    formulastring+="]"
  else:
    #There is an extra comma on the end.  Remove comma.  Add end bracket.
    formulastring = formulastring[:-1]
    formulastring+="]"

  try:
    if sys.argv[1] == "TEST":
      formulastring = testFormulaString
    f = json.loads(formulastring)
    assert is_well_formed(f)
    v = solve_dfs(f)

    #Most consuming of CPU based on cProfile
    #DO NOT USE, bugged v = solve_dimacs_formula(f,pp,trace)
    #v = solve_dpll(f,trace)  BROKEN
    
  except ValueError:
    print "Could not interpret '%s' as file or formula" % formulastring

  if v == False:
    numunsats+=1
    if numClauses < 18:
      print "Unsat"
      print formulastring
      print numClauses
  #else:
  #    print formulastring
  #    print v

unsatratio = float(numunsats)/iter
print "Ratio of unsatisfiable to satisfiable formulas (unless this is a test)"
print unsatratio

#return 1
#solve_dimacs_formula([[1,-3],[2,3,-1]], True, True)
#solve_dimacs_formula(formulastring,pp,trace)
