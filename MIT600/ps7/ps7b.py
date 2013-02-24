import random

def stdDev(X):
    mean = sum(X)/float(len(X))
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    return (tot/len(X))**0.5

def Yahtzee(numTests):
    total = 0.0
    
    for i in range(numTests):
        issame = 1
        num_list = list()
        for d in range(5):
            num_list.append(random.randint(1,6))
        for num in range(4):
            if num_list[num] != num_list[num+1]:
                issame = 0
                break
        if issame == 1:
            total += 1
    return (total / numTests) * 100

def Yahtzeetrials(numTrials, numTests):
    tests = list()
    for i in range(numTrials):
        tests = Yhatzee(numTests)


print '1000000 tests', Yahtzee(100000), '%'
