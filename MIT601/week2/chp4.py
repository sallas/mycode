class SM:
    startState = None
    def start(self):
        self.state = self.startState
    def step(self, inp, verbose=False):
        (s, o) = self.getNextValues(self.state, inp)
        if verbose: print "In: " + str(inp) + " Out: " + str(o) + \
                       " Next State: " + str(s)
        self.state = s
        return o
    def transduce(self, inputs, verbose=False):
        self.start()
        if verbose: print "Start state: " + str(self.startState)
        output = []
        for inp in inputs:
            output.append(self.step(inp, verbose))
            if self.done(self.state):
                break
        return output
                
    def run(self, n=10):
        return self.transduce([None]*n)
    # defualt methods that most likely will be overriden by subclasses
    def getNextValues(self, state , inp):
        nextState = self.getNextState(state, inp)
        return (nextState, nextState)
    def done(self, state):
        return False

class Accumulator(SM):
    def __init__(self, start=0):
        self.startState = start
    def getNextState(self, state , inp):
        return state + inp

class Gain(SM):
    def __init__(self, k):
        self.k = k
    def getNextState(self, state, inp):
        return inp * self.k

class ABC(SM):
    startState = 0
    def getNextValues(self, state, inp):
        if state == 0 and inp == 'a':
            return (1,True)
        elif state == 1 and inp == 'b':
            return (2,True)
        elif state == 2 and inp == 'c':
            return (0, True)
        else:
            return (3,False)

class UpDown(SM):
    startState = 0
    def getNextState(self, state, inp):
        if inp == 'u':
            return state +1
        else:
            return state -1


class Delay(SM):
    def __init__(self, start=0):
        self.startState = start
    def getNextValues(self, state , inp):
        return (inp, state)

class Average2(SM):
    startState = 0
    def getNextValues(self, state, inp):
        return (inp, (inp + state) / 2.0)

class SumLast3(SM):
    startState = (0,0)
    def getNextValues(self, state ,inp):
        (previousPreviousInput, previousInput) = state
        return ((previousInput, inp),
                previousPreviousInput + previousInput + inp)
    
class Select(SM):
    def __init__(self,k):
        self.k = k
    def getNextState(self, state, inp):
        return inp[self.k]

class SimpleParkingGate(SM):
    startState = 'waiting'

    def generateOutput(self, state):
        if state == 'raising':
            return 'raise'
        elif state == 'lowering':
            return 'lower'
        else:
            return 'nop'

    def getNextValues(self, state, inp):
        (gatePosition, carAtGate, carJustExited) = inp
        if state == 'waiting' and carAtGate:
            nextState = 'raising'
        elif state == 'raising' and gatePosition == 'top':
            nextState = 'raised'
        elif state == 'raised' and carJustExited:
            nextState = 'lowering'
        elif state == 'lowering' and gatePosition == 'bottom':
            nextState = 'waiting'
        else:
            nextState = state
        return (nextState, self.generateOutput(nextState))

class Increment(SM):
    def __init__(self, incr):
        self.incr = incr
    def getNextState(self, state, inp):
        return safeAdd(inp, self.incr)

class Parallel(SM):
    def __init__(self, sm1, sm2):
        self.m1 = sm1
        self.m2 = sm2
        self.startState = (sm1.startState, sm2.startState)
    def getNextValues(self, state, inp):
        (s1, s2) = state
        (newS1, o1) = self.m1.getNextValues(s1, inp)
        (newS2, o2) = self.m2.getNextValues(s2, inp)
        return ((newS1, newS2), (o1, o2))

class Parallel2(Parallel):
    def getNextValues(self, state, inp):
        (s1, s2) = state
        (i1, i2) = splitValue(inp)
        (newS1, o1) = self.m1.getNextValues(s1, i1)
        (newS2, o2) = self.m2.getNextValues(s2, i2)
        return ((newS1, newS2), (o1, o2))

class ParallelAdd(Parallel):
    def getNextValues(self, state, inp):
        (s1, s2) = state
        (newS1, o1) = self.m1.getNextValues(s1, inp)
        (newS2, o2) = self.m2.getNextValues(s2, inp)
        return ((newS1, newS2), o1 + o2)

class Feedback(SM):
    def __init__(self, sm):
        self.m = sm
        self.startState = self.m.startState
    def getNextValues(self, state, inp):
        (ignore, o) = self.m.getNextValues(state, 'undefined')
        (newS, ignore) = self.m.getNextValues(state, o)
        return (newS, o)

class CharTSM(SM):
    startSate = False
    def __init__(self, c):
        self.c = c
    def getNextValues(self, state, inp):
        return (True, self.c)
    def done(self, state):
        return state

class ConsumeFiveValues(SM):
    startState = (0, 0)
    def getNextValues(self,state, inp):
        (count, total) = state
        if count == 4:
            return ((count + 1, total + inp), total + inp)
        else:
            return ((count + 1, total + inp), None)
        def done(self, state):
            (count, total) = state
            return count == 5

class Repeat(SM):
    def __init__(self , sm, n = None):
        self.sm = sm
        self.startState = (0, self.sm.startState)
        self.n = n
    def advanceIfDone(self, counter , smState):
        while self.sm.done(smState) and not self.done((counter, smState)):
            counter = counter + 1
            smState = self.sm.startState
        return (counter, smState)
    def getNextValues(self, state, inp):
        (counter, smState) = state
        (smState, o) = self.sm.getNextValues(smState, inp)
        (counter, smState) = self.advanceIfDone(counter, smState)
        return ((counter, smState), o)
    def done(self, state):
        (counter, smState) = state
        return counter == self.n

class Sequence(SM):
    def __init__(self, smList):
        self.smList = smList
        self.startState = (0, self.smList[0].startState)
        self.n = len(smList)
    def advanceIfDone(self, counter, smState):
        while self.smList[counter].done(smState) and counter + 1 < self.n:
            counter = counter + 1
            smState = self.smList[counter].startState
        return (counter, smState)
    def getNextValues(self, state, inp):
        (counter, smState) = state
        (smState, o) = self.smList[counter].getNextValues(smState, inp)
        (counter, smState) = self.advanceIfDone(counter, smState)
        return ((counter, smState), o)
    def done(self, state):
        (counter, smState) = state
        return self.smList[counter].done(smState)

class RepeatUntil(SM):
    def __init__(self, condition, sm):
        self.sm = sm
        self.condition = condition
        self.startState = (False, self.sm.startState)

    def getNextValues(self, state, inp):
        (condTrue, smState) = state
        (smState, o) = self.sm.getNextValues(smState, inp)
        condTrue = self.condition(inp)
        if self.sm.done(smState) and not condTrue:
            smState = self.sm.getStartState()
        return ((condTrue, smState), o)

    def done(self, state):
        (condTrue, smState) = state
        return self.sm.done(smState) and condTrue

class Until(SM):
    def __init__(self,condition, sm):
        self.sm = sm
        self.condition = condition
        self.startState = (False, self.sm.startState)
    def getNextValues(self, state, inp):
        pass
    
class MySM(SM):
    startState = (0,0)
    def getNextValues(self, state, inp):
        (x, y) = state
        y += inp
        if y >= 100:
            return ((x + 1, 0), y)
        return ((x, y), y)
    def done(self, state):
        (x, y) = state
        return x >= 3

class Sum(SM):
    startState = 0
    def getNextValues(self, state, inp):
        nextState = state + inp
        return (nextState, nextState)
    def done(self, state):
        return state >= 100

class CountingStateMachine(SM):
    startState = 0
    def getNextValues(self, state, inp):
        return (state + 1, self.getOutput(state, inp))
    
class CountMod5(CountingStateMachine):
    def getOutput(self, state, inp):
        return state % 5

class AlternateZeros(CountingStateMachine):
    def getOutput(self, state, inp):
        return (state%2) ? x : 0
        if not state%2:
            return inp
        return 0

def makeCounter(init, step):
    return Feedback(Cascade(Increment(step), Delay(init)))

def splitValue(v):
    if v== 'undefined':
        return ('undefined', 'undefined')
    else:
        return v

def safeAdd(x, y):
    if x == 'undefined' or y == 'undefined':
        return 'undefined'
    else:
        return x + y

def safeMul(x, y):
    if x == 'undefined' or y == 'undefined':
        return 'undefined'
    else:
        return x * y
    


def main():
    pass

if __name__ == "__main__":
    main()
