

class MySM:
    startState = (0,0)
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
    
    def getNextValues(self, state , inp):
        (counter, state2) = state
        output = state2 + inp
        if output >= 100:
            nextState = 0
            counter += 1
        else:
            nextState = output

        return ((counter, nextState), output)
    
    def getNextState(self, state , inp):
        return state + inp
    def done(self, state):
        (counter, state2) = state
        return counter >= 3
        
