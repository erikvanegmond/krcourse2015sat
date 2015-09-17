# import argparse
import random
import csv
import os
import pycosat
from pprint import pformat
from pprint import pprint



##=============================

#
qqgencmd = 'qqwing --stats --timer --csv --solution --count-solutions --generate %s'
qqgencmd = 'qqwing --stats --csv --solution --count-solutions --generate %s'


# ./qqwing --generate 100 --stats --timer --csv
#
# qqgencmd = './qqwing --generate 10 --stats --timer --csv --solution --count-solutions'
#
# qqquerycmd = '.qqwing --solve

def sudokus_from_csvfileobj(f):
    print "to sudoku Object..."
    sudokus = []

    c = csv.DictReader(f)
    for r in c:
        sudokus.append( Sudoku( r['Puzzle'],
                                solution=r['Solution'],
                                difficulty=r['Difficulty'],
                                numgivens=int(r['Givens']),
                                # gentime=r['Time (milliseconds)'],
                                numsolutions=r['Solution Count'] ))
    return sudokus

def import_sudokus_from_file(filename):

    with open(filename) as f:
        return sudokus_from_csvfileobj(f)


# can add more parameters later to this generate function
def generate_sudokus(num=1):
    with os.popen( qqgencmd % (num) ) as f:
        print "sudokus generated..."
        return sudokus_from_csvfileobj(f)

def oneline_to_satvars(s):

    givens = []
    rows = [list(s[i:i+9]) for i in range(0,81,9)]
    r = 1
    for row in rows:
        for c in range(9):
            if row[c] != '.':
                givens.append(str(r)+str(c+1)+row[c])
                # print givens[-1], v(r,c+1, int(row[c]))
        r += 1
    return givens


def v(i, j, d):
    """
    Return the number of the variable of cell i, j and digit d,
    which is an integer in the range of 1 to 729 (including).
    """
    return 81 * (i - 1) + 9 * (j - 1) + d

def solution_vars_to_oneline(s):

    s.sort()  # (to be safe)

    return ''.join( [v[2] for v in s] )


def sudoku_clauses():
    """
    Create the (11745) Sudoku clauses, and return them as a list.
    Note that these clauses are *independent* of the particular
    Sudoku puzzle at hand.
    """
    res = []
    # for all cells, ensure that the each cell:
    for i in range(1, 10):
        for j in range(1, 10):
            # denotes (at least) one of the 9 digits (1 clause)
            res.append([v(i, j, d) for d in range(1, 10)])
            # does not denote two different digits at once (36 clauses)
            for d in range(1, 10):
                for dp in range(d + 1, 10):
                    res.append([-v(i, j, d), -v(i, j, dp)])

    def valid(cells):
        # Append 324 clauses, corresponding to 9 cells, to the result.
        # The 9 cells are represented by a list tuples.  The new clauses
        # ensure that the cells contain distinct values.
        for i, xi in enumerate(cells):
            for j, xj in enumerate(cells):
                if i < j:
                    for d in range(1, 10):
                        res.append([-v(xi[0], xi[1], d), -v(xj[0], xj[1], d)])

    # ensure rows and columns have distinct values
    for i in range(1, 10):
        valid([(i, j) for j in range(1, 10)])
        valid([(j, i) for j in range(1, 10)])
    # ensure 3x3 sub-grids "regions" have distinct values
    for i in 1, 4, 7:
        for j in 1, 4 ,7:
            valid([(i + k % 3, j + k // 3) for k in range(9)])

    assert len(res) == 81 * (1 + 36) + 27 * 324
    return res


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

    def givens_to_dimacs_list(self):
        grid = [list(self.givens[i:i+9]) for i in range(0,81,9)]
        clauses = []#sudoku_clauses()
        for i in range(1, 10):
            for j in range(1, 10):
                d = grid[i - 1][j - 1]
                try:
                    clauses.append([v(i, j, int(d))])
                except ValueError:
                    continue
        return clauses

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
        return Sudoku(''.join(givenslist), self.solution, numgivens=newnumgivens, difficulty=self.difficulty)


    def new_sudoku_more_givens(self, incr=1):

        givenslist = list(self.givens)
        newnumgivens = self.numgivens + incr

        while incr > 0:
            i = random.randint(0,80)
            if givenslist[i] == '.':
                givenslist[i] = self.solution[i]
                incr -= 1

        return Sudoku(''.join(givenslist), self.solution, numgivens=newnumgivens)

    def getSolution(self):
        return Sudoku(self.solution, self.solution, numgivens=81, difficulty=self.difficulty)

    def proper(self):
        baseClauses = sudoku_clauses()
        totalClauses = baseClauses + self.givens_to_dimacs_list()

        sol = set(pycosat.solve(totalClauses))

        def read_cell(i, j):
            for d in range(1, 10):
                if v(i, j, d) in sol:
                    return [v(i, j, d),d]

        negation = []
        for i in range(1, 10):
            for j in range(1, 10):
                negation.append(-read_cell(i, j)[0])

        totalClauses.append(negation)
        res = pycosat.solve(totalClauses)
        if res == "UNSAT":
            return 1
        else:
            return 0

    def __str__(self):
        grid = [list(self.givens[i:i+9]) for i in range(0,81,9)]
        return pformat(grid)

diff = {"Simple":1,"Easy":2, "Intermediate":3, "Expert":4}

while True:
    sudokus = generate_sudokus(100)
    f = open('data.csv', 'a')
    sudokuCounter = 0
    for sudoku in sudokus:
        sudokuCounter+=1
        print sudokuCounter
        curSudoku = sudoku.getSolution()
        results = ""
        for i in range(curSudoku.numgivens):
            #difficulty,givens,proper
            results += "%s,%s,%s\n" % (diff[curSudoku.difficulty], curSudoku.numgivens, curSudoku.proper())
            curSudoku = curSudoku.new_sudoku_fewer_givens(1)
        f.write(results)





