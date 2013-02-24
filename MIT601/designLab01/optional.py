def evenSquares(sList):
    return [ x**2  for x in sList if x % 2 == 0 ]

def sumAbsProd(first, second):
    return sum([   abs(x)  for x in first  * sum([ abs(y) for y in second ])])

def testsum(first,second):
    total = 0
    for x in first:
        for y in second:
            total += abs(x)*abs(y)
    return total

def extractTags(string):
    wordList = []
    for i in xrange(len(string)):
        if string[i] == "[":
            save = i
        elif string[i] == "]":
            wordList.append(string[save+1:i])
    return wordList

class FruitSalad:
    fruits = ['melons','pineapples']
    servings = 4
    def __init__(self, ingredients, numservings):
        self.fruits += ingredients
        self.servings = numservings
    def __str__(self):
        return str(self.servings) + " servings of fruit salad with " + str(self.fruits)
    def server(self):
        if self.servings <= 0:
            print "sorry"
        else:
            print "enjoy"
            self.servings -= 1

def warehouseProcess(goods, transaction):
    transactionType, item, quantity = transaction
    if transactionType == 'ship':
        goods[item] -= quantity
    else:
        if item in goods:
            goods[item] += quantity
        else:
            goods[item] = quantity

class Warehouse:
    def __init__(self):
        self.inventory = {}
    def process(self, transaction):
        warehouseProcess(self.inventory, transaction)
    def lookup(self, item):
        if item in self.inventory:
            return self.inventory[item]
        else:
            return 0





        

    
