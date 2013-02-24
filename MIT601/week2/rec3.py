def square(x):
    return x*x

def selfComposition2(someFunction, x=0):
    def returnFunction(*args):
        def returnFunction2(*args):
            def returnFunction3(*args):
                def returnFunction4(*args):
                    def returnFunction5(*args):
                        def returnFunction6(*args):
                            def returnFunction7(*args):
                                return someFunction(someFunction(*args))
                            return returnFunction7(*args)
                        return returnFunction6(*args)
                    return returnFunction5(*args)
                return returnFunction4(*args)
            return returnFunction3(*args)
        return returnFunction2(*args)
    return returnFunction

def selfComposition(someFunction):
    def returnFunction(*args):
        return someFunction(someFunction(*args))
    return returnFunction
