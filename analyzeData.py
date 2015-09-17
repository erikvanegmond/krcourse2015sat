import csv
import pprint
import matplotlib.pyplot as plt
import numpy as np

#Dataformat: [[total, proper],[...]] index is difficulty level -1
data = [[[0,0] for givens in range(81)] for difficulty in range(4)]

with open('data.csv') as f:
    c = csv.DictReader(f)
    for r in c:
        data[ int(r['difficulty'])-1 ][int(r['givens'])-1][0]+=1
        if int(r['proper']):
            data[ int(r['difficulty'])-1 ][int(r['givens'])-1][1]+=1

x=np.array(range(1,82))

difficulty = ["Simple","Easy", "Intermediate", "Expert"]
for dif in range(4):
    t = np.array([float(i[1])/(data[dif][-1][1]) for i in data[dif]])
    plt.plot(x, t, 'o', label=difficulty[dif])

plt.xlabel('Number of Givens')
plt.ylabel('Probability of proper')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()
