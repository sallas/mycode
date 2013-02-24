#
# File:   designLab01Work.py
# Author: 6.01 Staff
# Date:   02-Sep-11
#
# Below are templates for your answers to three parts of Design Lab 1

#-----------------------------------------------------------------------------

def fib(n):
    if n < 0:
        print "BUGGER OFF YOU FUCKER DON*T TRY AND MESS WITH MY PROGRAM"
        return 1029083289073179
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1)+fib(n-2)

#-----------------------------------------------------------------------------

class V2:
    def __init__(self, x, y):
        self.vector = (x , y)
    def __str__(self):
        return "V2[" + str(self.vector[0]) + ", " + str(self.vector[1]) + "]"
    def getX(self):
        return self.vector[0]
    def getY(self):
        return self.vector[1]
    def add(self, v):
        return self.vector[0] + v.vector[0] , self.vector[1] + v.vector[1]
    def __add__(self, v):
        return self.add(v)
    def mul(self, v):
        return self.vector[0] * v.vector[0] , self.vector[1] * v.vector[1]
    def __mul__(self, v):
        return self.mul(v)

#-----------------------------------------------------------------------------
class Polynomial:
    def __init__(self, coefficients):
        self.coeffs = [ float(coeff) for coeff in coefficients ]
        self.coeffs.reverse()
        self.size = len(self.coeffs)
    def coeff(self, i):
        return self.coeffs[i-1]

    
    def __str__(self):
        string = ""
        for i in xrange(self.size - 1, -1, -1):

            if i == self.size - 1:
                pass
            elif self.coeffs[i] == 0:
                continue
            elif self.coeffs[i] > 0:
                string += " + "
            else:
                string += " "
            if i == 0:
                string += str(self.coeffs[i])
            elif i == 1:
                string += str(self.coeffs[i]) + " z"
            else:
                string +=  str(self.coeffs[i]) + " z**" + str(i)
        return string
            
    def add(self, p):
        if self.size >= p.size:
            maxExp = p.size
            newPolyList = self.coeffs[:]
        else:
            maxExp = self.size
            newPolyList = p.coeffs[:]
        for i in xrange(maxExp):
            newPolyList[i] += p.coeffs[i]
        newPolyList.reverse()
        return Polynomial(newPolyList)
            
    def __add__(self, p):
        return self.add(p)
    
    def mul(self, p):
        mulList = []
        maxExp = self.size + p.size - 1
        for unused_i in xrange(maxExp):
            mulList.append(0)
        for i in xrange(self.size):
            for j in xrange(p.size):
                mulList[i+j] += self.coeffs[i] * p.coeffs[j]
        mulList.reverse()
        return Polynomial(mulList)
    
    def __mul__(self, p):
        return self.mul(p)
    def val(self, v):
        total = 0
        for i in xrange(self.size):
            total += v**i * self.coeffs[i]
        return total
    def __repr__(self):
        return str(self)
    def __call__(self, x):
        return self.val(x)
    def roots(self):
        if self.size > 3:
            print "Order too high to solve for roots."
            return
        if self.size == 1:
            print "that isn't even a polynomial dork"
            return
        
        if self.size == 2:
            return -(self.coeffs[0]/self.coeffs[1])

        if self.size == 3:
            number = self.coeffs[1]**2-4*self.coeffs[2]*self.coeffs[0]
            if number < 0:
                number = complex(number)**0.5
            else:
                number = number**0.5
            root1 = (-self.coeffs[1]-number)/(2*self.coeffs[2])
            root2 = (-self.coeffs[1]+number)/(2*self.coeffs[2])
            return [root1, root2]
    def hornerval(self, v, n=-1):
        result = 0
        co = self.coeffs[:]
        co.reverse()
        for coeff in co:
            result = result * v + coeff
        return result
        
        
    

