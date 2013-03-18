


F1 = 'simple.vector'
F2 = 'simple.vector.out'


l1 = []
for line in open(F1):
    l1.append(line.split(' ')[0])

l2 = []
for line in open(F2):
    l2.append(line.split(' ')[0])

for i in range(len(l1)):
    print l1[i],l2[i]
