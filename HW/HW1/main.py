'''
Created on 2018.09.07
Author: Donggyu Kim
'''

import math


class Func:  # superclass of all three function classes(Exp,Cubic,Log)
    def __init__(self,a,b):  # Exp and Log functions don't use c,d
        self.a=a
        self.b=b

    def eval(self,x):  # evaluate / abstract
        pass

    def deriv(self,x):  # derivative / abstract
        pass

    def binarySearch(self,low,high,tol):
        print("Binary Search")
        if self.eval(low) * self.eval(high) > 0:
            print("Can't find in this range!")
            return
        cnt=1
        mid=(low+high)/2
        while abs(self.eval(mid))>tol:
            cnt+=1
            if self.eval(low)*self.eval(mid)>0:
                low=mid
            else:
                high=mid
            mid=(low+high)/2
        print("Solution : f(",mid,") = ",self.eval(mid)," after ",cnt," iterations")

    def newtonSearch(self,x0,tol):
        print("Newton Search")
        x=x0
        cnt=1
        while abs(self.eval(x))>tol:
            cnt+=1
            x0=x
            x=x0-self.eval(x0)/self.deriv(x0)
        print("Solution : f(", x, ") = ", self.eval(x), " after ", cnt, " iterations")

    def secantSearch(self,x0,x1,tol):
        print("Secant Search")
        x=x1-self.eval(x1)*(x1-x0)/(self.eval(x1)-self.eval(x0))
        cnt=1
        while abs(self.eval(x))>tol:
            cnt+=1
            x0=x1
            x1=x
            x=x1-self.eval(x1)*(x1-x0)/(self.eval(x1)-self.eval(x0))
        print("Solution : f(", x, ") = ", self.eval(x), " after ", cnt, " iterations")

    def printFunction(self):  # abstract
        pass


class ExpFunc(Func):
    def eval(self,x):
        return self.a*math.exp(x)+self.b

    def deriv(self,x):
        return self.a*math.exp(x)

    def printFunction(self):
        print("f(x) = ",self.a," * exp(x) + ",self.b)


class CubicFunc(Func):
    def __init__(self,a,b,c,d):  # method overriding
        super(CubicFunc,self).__init__(a,b)
        self.c=c
        self.d=d

    def eval(self,x):
        return self.a*(x**3)+self.b*(x**2)+self.c*x+self.d

    def deriv(self,x):
        return 3*self.a*(x**2)+2*self.b*x+self.c

    def printFunction(self):
        print("f(x) = ",self.a," * x^3 + ",self.b," * x^2 + ",self.c," * x + ",self.d)


class LogFunc(Func):
    def eval(self,x):
        return self.a*math.log(x)+self.b

    def deriv(self,x):
        return self.a/x

    def printFunction(self):
        print("f(x) = ",self.a," * log(x) + ",self.b)


funcExp=ExpFunc(3.0,-5.0)
funcCubic=CubicFunc(2,-3,4,-5)
funcLog=LogFunc(3.0,10.0)

funcExp.printFunction()
funcExp.binarySearch(-10,10,0)
funcExp.newtonSearch(0,0)
funcExp.secantSearch(0,10,0)
print("\n")

funcCubic.printFunction()
funcCubic.binarySearch(-10,10,1e-5)
funcCubic.newtonSearch(0,1e-5)
funcCubic.secantSearch(0,10,1e-5)
print("\n")

funcLog.printFunction()
funcLog.binarySearch(0.00001,10,0) # low must be bigger than 0 to avoid trying to evaluate log(x) s.t. x<0
# Can't use Newton's search
funcLog.secantSearch(0.00001,0.001,0) # how can we find proper x0 and x1, that makes x_i doesn't go under 0?
