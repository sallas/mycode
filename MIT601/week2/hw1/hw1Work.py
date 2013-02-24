import pdb
import lib601.sm as sm
import string
import operator

class BinaryOp:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return self.opStr + '(' + \
               str(self.left) + ', ' +\
               str(self.right) + ')'
    __repr__ = __str__

class Sum(BinaryOp):
    opStr = 'Sum'
    def eval(self, env):
        return self.left.eval(env) + self.right.eval(env)

class Prod(BinaryOp):
    opStr = 'Prod'
    def eval(self, env):
        return self.left.eval(env) * self.right.eval(env)

class Quot(BinaryOp):
    opStr = 'Quot'
    def eval(self, env):
        return self.left.eval(env) / self.right.eval(env)

class Diff(BinaryOp):
    opStr = 'Diff'
    def eval(self, env):
        return self.left.eval(env) - self.right.eval(env)

class Assign(BinaryOp):
    opStr = 'Assign'
    def eval(self, env):
        env[self.left.name] = self.right.eval(env)
        
class Number:
    def __init__(self, val):
        self.value = val
    def __str__(self):
        return 'Num('+str(self.value)+')'
    __repr__ = __str__
    
    def eval(self, env):
        return self.value

class Variable:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'Var('+self.name+')'
    __repr__ = __str__
    
    def eval(self, env):
        if self.name in env:
            return env[self.name]
        return False



# characters that are single-character tokens
seps = ['(', ')', '+', '-', '*', '/', '=']

# Tokenizer state machine
class Tokenizer(sm.SM):
    startState = ""
    def getNextValues(self, state, inp):
        if inp == " ":
            output = state
            nextState = ""
        elif inp in seps:
            output = state
            nextState = inp
        elif state in seps:
            output = state
            nextState = inp    
        else:
            nextState = state + inp
            output = ""
        return (nextState, output)

def tokenize(inputString):
    inputString += " "
    tokens = Tokenizer().transduce(inputString)
    return [ t for t in tokens if t != ""]
    

# Convert strings into a list of tokens (strings)
def tokenize2(string):
    tempString = ""
    tokenList = []
    for c in string:
        if c in seps:
            if len(tempString) > 0:
                tokenList.append(tempString)
                tempString = ""
            tokenList.append(c)
        elif c == ' ':
            if len(tempString) > 0:
                tokenList.append(tempString)
                tempString = ""
        else:
            tempString += c
    if len(tempString) > 0:
        tokenList.append(tempString)
    return tokenList


    

# tokens is a list of tokens
# returns a syntax tree:  an instance of {\tt Number}, {\tt Variable},
# or one of the subclasses of {\tt BinaryOp} 
def parse(tokens):
    def parseExp(index):
        if numberTok(tokens[index]):
            return (Number(float(tokens[index])), index + 1)
        elif variableTok(tokens[index]):
            return (Variable(tokens[index]), index + 1)
        else:
            (leftTree, nextIndex) = parseExp(index + 1)
            op = tokens[nextIndex]
            (rightTree, nextIndex) = parseExp(nextIndex +1)
            if op == '+':
                return (Sum(leftTree, rightTree), nextIndex + 1)
            elif op == '-':
                return (Diff(leftTree, rightTree), nextIndex + 1)
            elif op == '*':
                return (Prod(leftTree, rightTree), nextIndex + 1)
            elif op == '=':
                return (Assign(leftTree, rightTree), nextIndex + 1)
            else:
                return (Quot(leftTree, rightTree), nextIndex +1)
            
    (parsedExp, nextIndex) = parseExp(0)
    return parsedExp

# token is a string
# returns True if contains only digits
def numberTok(token):
    for char in token:
        if not char in string.digits: return False
    return True

# token is a string
# returns True its first character is a letter
def variableTok(token):
    for char in token:
        if char in string.letters: return True
    return False

# thing is any Python entity
# returns True if it is a number
def isNum(thing):
    return type(thing) == int or type(thing) == float

# Run calculator interactively
def calc():
    env = {}
    while True:
        e = raw_input('%')            # prints %, returns user input
        print '%', # your expression here
        print '   env =', env

# exprs is a list of strings
# runs calculator on those strings, in sequence, using the same environment
def calcTest(exprs):
    env = {}
    for e in exprs:
        print '%', e                    # e is the experession
        t = tokenize(e)
        p = parse(t)
        p.eval(env)
        print p.eval(env)
        print '   env =', env

# Simple tokenizer tests
'''Answers are:
['fred']
['777']
['777', 'hi', '33']
['*', '*', '-', ')', '(']
['(', 'hi', '*', 'ho', ')']
['(', 'fred', '+', 'george', ')']
['(', 'hi', '*', 'ho', ')']
['(', 'fred', '+', 'george', ')']
'''
def testTokenize():
    print tokenize('fred ')
    print tokenize('777 ')
    print tokenize('777 hi 33 ')
    print tokenize('**-)(')
    print tokenize('( hi * ho )')
    print tokenize('(fred + george)')
    print tokenize('(hi*ho)')
    print tokenize('( fred+george )')


# Simple parsing tests from the handout
'''Answers are:
Var(a)
Num(888.0)
Sum(Var(fred), Var(george))
Quot(Prod(Var(a), Var(b)), Diff(Var(cee), Var(doh)))
Quot(Prod(Var(a), Var(b)), Diff(Var(cee), Var(doh)))
Assign(Var(a), Prod(Num(3.0), Num(5.0)))
'''
def testParse():
    print parse(['a'])
    print parse(['888'])
    print parse(['(', 'fred', '+', 'george', ')'])
    print parse(['(', '(', 'a', '*', 'b', ')', '/', '(', 'cee', '-', 'doh', ')' ,')'])
    print parse(tokenize('((a * b) / (cee - doh))'))
    print parse(tokenize('(a = (3 * 5))'))

####################################################################
# Test cases for EAGER evaluator
####################################################################

def testEval():
    env = {}
    Assign(Variable('a'), Number(5.0)).eval(env)
    print Variable('a').eval(env)
    env['b'] = 2.0
    print Variable('b').eval(env)
    env['c'] = 4.0
    print Variable('c').eval(env)
    print Sum(Variable('a'), Variable('b')).eval(env)
    print Sum(Diff(Variable('a'), Variable('c')), Variable('b')).eval(env)
    Assign(Variable('a'), Sum(Variable('a'), Variable('b'))).eval(env)
    print Variable('a').eval(env)
    print env

# Basic calculator test cases (see handout)
testExprs = ['(2 + 5)',
             '(z = 6)',
             'z',
             '(w = (z + 1))',
             'w'
             ]
# calcTest(testExprs)

####################################################################
# Test cases for LAZY evaluator
####################################################################

# Simple lazy eval test cases from handout
'''Answers are:
Sum(Var(b), Var(c))
Sum(2.0, Var(c))
6.0
'''
def testLazyEval():
    env = {}
    Assign(Variable('a'), Sum(Variable('b'), Variable('c'))).eval(env)
    print Variable('a').eval(env)
    env['b'] = Number(2.0)
    print Variable('a').eval(env)
    env['c'] = Number(4.0)
    print Variable('a').eval(env)

# Lazy partial eval test cases (see handout)
lazyTestExprs = ['(a = (b + c))',
                  '(b = ((d * e) / 2))',
                  'a',
                  '(d = 6)',
                  '(e = 5)',
                  'a',
                  '(c = 9)',
                  'a',
                  '(d = 2)',
                  'a']
# calcTest(lazyTestExprs)

## More test cases (see handout)
partialTestExprs = ['(z = (y + w))',
                    'z',
                    '(y = 2)',
                    'z',
                    '(w = 4)',
                    'z',
                    '(w = 100)',
                    'z']

# calcTest(partialTestExprs)
