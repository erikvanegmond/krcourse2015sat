

# import argparse

import random

import csv

import os


##=============================

#
qqgencmd = './qqwing --stats --timer --csv --solution --count-solutions --generate '





def sudokus_from_csvfileobj(f):

    sudokus = []
    
    c = csv.DictReader(f)

    for r in c:
        sudokus.append( Sudoku( r['Puzzle'], solution=r['Solution'], difficulty=r['Difficulty'],
                                numgivens=r['Givens'], gentime=r['Time (milliseconds)'],
                                numsolutions=r['Solution Count'] ))

    return sudokus



def import_sudokus_from_file(filename):

    with open(filename) as f:
        return sudokus_from_csvfileobj(f)





# can add more parameters later to this generate function
def generate_sudokus(num=1):

    with os.popen( qqgencmd + str(num) ) as f:
        return sudokus_from_csvfileobj(f)




























def oneline_to_satvars(s):
    
    givens = []
    rows = [list(s[i:i+9]) for i in range(0,81,9)]
    r = 1
    
    for row in rows:
        for c in range(9):
            if row[c] != '.':
                givens.append(str(r)+str(c+1)+row[c])
        r += 1

    return givens



def solution_vars_to_oneline(s):
    
    s.sort()  # (to be safe)

    return ''.join( [v[2] for v in s] )


















class Sudoku(object):

    def __init__(self, givens, solution=None, difficulty=None, stats={},
                 numgivens=None, numsolutions=None, gentime=None):

        # givens and solution are 81-char strings
        self.givens = givens
        self.solution = solution
        
        self.difficulty = difficulty

        self.numgivens = numgivens

        self.stats = stats
        





    def check_difficulty(self):
        # query qqwing with self.givens
        return

    def check_numsolutions(self):
        # query qqwing with self.givens
        return





    

    def givens_to_dimacs(self):
        return '\n'.join(map((lambda x: x + ' 0'), oneline_to_satvars(self.givens)))

    def dimacs_to_solution(self, sat):
        # input string describing successful SAT instance (729 variables)
        
        return ''.join([i[2] for i in list(filter((lambda x: x[0] != '-'), sat.split(' '))).sort()])






    


    def new_sudoku_fewer_givens(self, decr=1):

        givenslist = list(self.givens)
        newnumgivens = self.numgivens - decr

        while decr > 0:
            i = random.randint(0,80)
            if givenslist[i] != '.':
                givenslist[i] = '.'
                decr -= 1
        
        return Sudoku(''.join(givenslist), self.solution, numgivens=newnumgivens)


    def new_sudoku_more_givens(self, incr=1):

        givenslist = list(self.givens)
        newnumgivens = self.numgivens + incr
        
        while incr > 0:
            i = random.randint(0,80)
            if givenslist[i] == '.':
                givenslist[i] = self.solution[i]
                incr -= 1
        
        return Sudoku(''.join(givenslist), self.solution, numgivens=newnumgivens)











    
##########






#
# ./qqwing --generate 100 --stats --timer --csv
#
#
#
# qqgencmd = './qqwing --generate 10 --stats --timer --csv --solution --count-solutions'
#
# qqquerycmd = '.qqwing --solve
#
#
#
#
#
#
#
#


