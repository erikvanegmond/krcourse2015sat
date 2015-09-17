import csv
import pprint
import matplotlib.pyplot as plt
import numpy as np

def analyzeSolution(fname):
    #Dataformat: [[total, proper],[...]] index is difficulty level -1
    data = [[[0,0] for givens in range(81)] for difficulty in range(4)]

    with open(fname) as f:
        c = csv.DictReader(f)
        for r in c:
            data[ int(r['difficulty'])-1 ][int(r['givens'])-1][0]+=1
            if int(r['proper']):
                data[ int(r['difficulty'])-1 ][int(r['givens'])-1][1]+=1

    pprint.pprint(data)

    x=np.array(range(1,82))

    difficulty = ["Simple","Easy", "Intermediate", "Expert"]
    for dif in range(4):
        t = np.array([float(i[1])/(data[dif][-1][1]) for i in data[dif]])
        plt.plot(x, t, 'o', label=difficulty[dif])
        print "Difficulty: %s|| Mean:  %s, Variance: %s, Std: %s" % (difficulty[dif], np.mean(t),np.var(t),np.std(t))

    plt.xlabel('Number of Givens')
    plt.ylabel('Probability of proper')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()




def analyzeSudoku(fname):
    #Dataformat: [[total, proper],[...]] index is difficulty level -1
    data = [[[0,0] for givens in range(81)] for difficulty in range(4)]

    with open(fname) as f:
        c = csv.DictReader(f)
        for r in c:
            data[ int(r['difficulty'])-1 ][int(r['givens'])-1][0]+=1
            if int(r['proper']):
                data[ int(r['difficulty'])-1 ][int(r['givens'])-1][1]+=1

    pprint.pprint(data)

    x=np.array(range(1,82))

    difficulty = ["Simple","Easy", "Intermediate", "Expert"]
    for dif in range(4):
        t = np.array([float(i[1]) for i in data[dif]])
        plt.plot(x, t, 'o', label=difficulty[dif])

    plt.xlabel('Number of Givens')
    plt.ylabel('Probability of proper')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()

# analyzeSudoku('sudokuData.csv')
analyzeSolution('data.csv')