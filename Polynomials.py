class Polynomial:
    # method : __init__ /
    #  create a Polynomial object from string by spliting it by "+"
    def __init__(self, p="0"):
        # store the input string inside a variable for copying method
        self.input_str = str(p)
        # 1- remove all spaces
        # 2- replace all pow operators (**) with "^" to prevent split conflict when using `split("*")`
        # 3- replace sub "-" operators with "+-" to split the string into expressions with just `split("+")`
        self._expressions = str(p). \
            replace(" ", ""). \
            replace("**", "^"). \
            replace("-", "+-"). \
            strip("+*"). \
            split("+")
        
        self.expressions = list()
        self.parseExpressions()
        # re-Assemble the Polynomial once when creating!
        self.reassemble()
    
    # method : parseExpressions /
    #  create a Expression object from every expression string inside _expressions attr
    def parseExpressions(self):
        expressions = self._expressions
        for expression in expressions:
            self.expressions.append(Expression(expression))
    
    # method : getDerivativeBy /
    #  returns a Polynomial object that is a drivative from the Polynomial itself
    def getDrivativeBy(self, variable):
        result = Polynomial("0")
        # for every expression check if it has the variable inside then get the drivative, else just pass
        for exp in self.expressions:
            if variable in exp.data.get("Variables").keys():
                # call the getDrivativeBy(variable) from the Expression object
                result = result.__add__(exp.getDrivativeBy(variable))
            else:
                pass
        return result
    
    # method : copy /
    #  used to create a copy of the object
    def copy(self):
        st = self.input_str
        return Polynomial(str(self.input_str)+ "+0")
    
    # method : getMaxDepth /
    #  returns an int that is the maximum length of the tree
    #  by adding 1 to length of the longest expression
    def getMaxDepth(self):
        depths = list()
        for e in self.expressions:
            depths.append(e._len)
        return max(depths) + 2  # one to the root and one to the leaf
    
    # magic-method : __str__ /
    #  creating the result string for printing
    #  basically calls the magic-method `__str__` for every Expression object in the expressions attr
    def __str__(self):
        result = " + ".join([str(e) for e in self.expressions]). \
            replace(" + -", " - "). \
            rstrip(" +-")
        return result if result else "0"
    
    # magic-method : __add__ /
    #  simply the "+" operator!
    def __add__(self, other):
        if not type(other) is Polynomial:
            raise TypeError("")
        else:
            result = Polynomial(0)
            result.expressions.extend(other.copy().expressions)
            result.expressions.extend(self.copy().expressions)
            result.reassemble()
            return result
    
    # magic-method : __sub__ /
    #  simply the "-" operator!
    def __sub__(self, other):
        if not type(other) is Polynomial:
            raise TypeError("")
        else:
            other = other.copy()
            for exp in other.expressions:
                exp.C = int(-exp.C)
                exp._mkdata()
            result = Polynomial()
            result.expressions.extend(self.copy().expressions + other.expressions)
            result.reassemble()
            return result
    
    # method : reassemble /
    #  re-Assembles and simplifies the Polynomial by searching all similar expressions and adding their C together
    def reassemble(self):
        # get count of the expressions and strat from the first one
        l = len(self.expressions)
        i = 0
        while i < l:
            # then check the expressions after the `i` one if they are the same,
            # simply if they have same exponents for same variables
            j = i + 1
            while j < l:
                if self.expressions[i] == self.expressions[j]:
                    self.expressions[i].C += self.expressions[j].C
                    self.expressions[i]._mkdata()
                    del self.expressions[j]
                    # we deleted one object so we update the l value so we don't get the IndexError (index out of range)
                    l = len(self.expressions)
                    # if the other expression deleted we need to check if there are more similar expressions as well
                    j -= 1
                j += 1
            i += 1
        # after this we need to remove all zeros (C == 0) from the Polynomial
        i = 0
        while i < l:
            if self.expressions[i].C == 0:
                del self.expressions[i]
            i += 1
            l = len(self.expressions)
        self.input_str = str(self).replace("^", "**")

# class : Expression /
#  used to handle each expression inside expressions attr of Polynomial class
class Expression:
    # method : __init__ /
    #  create a Expression object from string by spliting it by "*"
    def __init__(self, expression: str):
        self._ves = expression.split("*")
        self.C = 0
        self.head = None
        self.data = dict()
        
        self._setC()
        self._len = len(self._ves)
        self.parseVaribles()
        self._mkdata()
    
    # method : _setC /
    #  detects the value of C (Coefficient) and assign it to c attr
    def _setC(self):
        tmp = self._ves[0]
        # check if negative
        if tmp.startswith("-"):
            if tmp[1].isdigit():
                try:
                    self.C = int(tmp)
                except:
                    exit("There is a problem with the input.")
                self._ves.pop(0)
            else:
                self.C = -1
                self._ves[0] = self._ves[0][1:]
        else:
            if tmp[0].isdigit():
                try:
                    self.C = int(tmp)
                except:
                    exit("There is a problem with the input.")
                self._ves.pop(0)
            else:
                self.C = 1
    
    # method : _mkdata /
    #  creates a data (dictionary) for the expression
    #  (used for checking the variable and exponents while getting drivative)
    def _mkdata(self):
        variables = dict()
        tmp = self.head
        while tmp:
            variables.update(tmp.data)
            tmp = tmp.next
        self.data = {
            "C": self.C,
            "Variables": variables
        }
    
    # magic-method : __str__ /
    #  returns a string ! creates the string with the data it has and makes the printing string more humanized
    def __str__(self):
        result = ""
        if self.C == -1:
            result += "-"
        elif self.C == 1:
            pass
        else:
            result += str(self.C)
        # start from the head and go to the end, get all variable with exponents as strings and add to the result string
        ve = self.head
        while ve:
            result += "*"+str(ve)
            ve = ve.next
        # strip the last "*"
        return result.strip(" *")
    
    # magic-method : __eq__ /
    #  compare to expression for equallity, check if the same variables have equal exponents
    def __eq__(self, other):
        if not type(other) is Expression:
            TypeError("")
        self_vars = self.data.get("Variables")
        other_vars = other.data.get("Variables")
        if not sorted(self_vars) == sorted(other_vars):
            return False
        for var in self_vars:
            if self_vars.get(var) != other_vars.get(var):
                return False
        return True
    
    # method : parseVaribles /
    #  after removing the coefficient we have just variables with exponents,
    #  after spliting them we create Variable objects and create a linked-list-like structure
    def parseVaribles(self):
        if not self._ves:
            return
        else:
            self.head = Variable(self._ves.pop(0))
            if not self._ves:
                return
            next_ve = self.head
            for ve in self._ves:
                next_ve.next = Variable(ve)
                next_ve = next_ve.next
    
    # method : getDrivativeBy /
    #  returns a Polynomial object from drivative of the expression,
    #  th reason for Polynomial object is that we need to add them to the result variable which is a Polynomial object too
    def getDrivativeBy(self, variable):
        data = self.data.copy()
        # if the exponent is 1
        if data.get("Variables").get(variable) == 1:
            # if this is our only variable
            if len(data.get("Variables")) == 1:
                return Polynomial(str(self.C))
            # in case there are other variables :
            else:
                del data["Variables"][variable]
                p = str(data["C"])
                for item in data.get("Variables").items():
                    p += "*" + str(item[0]) + "**" + str(item[1])
                return Polynomial(p)
        else:
            data["C"] *= data.get("Variables").get(variable)
            data["Variables"][variable] -= 1
            p = str(data["C"])
            for item in data.get("Variables").items():
                p += "*" + str(item[0]) + "**" + str(item[1])
            r = Polynomial(p)
            return r


# class : Variable /
#  the smallest part of the Polynomial, just variable with an exponent.
class Variable:
    def __init__(self, variable):
        ve = variable.split("^")
        self.v = ve[0]
        self.e = int(ve[1]) if len(ve) == 2 else 1
        self.data = {self.v: self.e}
        self._next = None
    
    # property : next /
    #  for controling the _next attr which is the next node and the next Variable with exponent
    @property
    def next(self):
        return self._next
    
    @next.setter
    def next(self, next_one):
        if not type(next_one) is Variable:
            return
        self._next = next_one
    
    # magic-method : __str__ /
    #  returns a humanized string of a variable and exponent
    def __str__(self):
        return self.v + "" if self.e == 1 else f"{self.v}^{self.e}"



p = Polynomial("x**2-x**2+2*x**2-x**2")
pc = p.copy()
print("Copy od p: ", pc)
print("Derivative by x: ", p.getDrivativeBy("x"))
print("Max depth: ", p.getMaxDepth())
p2 = Polynomial("x**2")
p3 = p-p2
print("p: ", p)
print("p2: ", p2)
print("p3: ", p3)
