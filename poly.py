from copy import deepcopy
from numpy import inf


class Variable(object):
    """
    Encapsulates variables and constants

    ex) x^3 or 5
    """
    def __init__(self, **kwargs):
        self.val = '1'  # name or const val
        self.power = 1  # float
        self.const = True  # bool
        # Priority of variable when sorting in descening or ascending
        self.priority = inf
        # True if sort in ascending, False for descending
        self.asc_desc = True

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __mul__(self, other):
        """
        x.__mul__(y) <==> x * y
        """

        if type(other) == int or type(other) == float:
            if self.const:
                return Variable(val=str(int(self.val)*other))
            raise Exception("Can only multiply a constant by a number")
        elif self.const and other.const:
            return Variable(val=str(int(self.val)*int(other.val)))
        elif not self.const and not other.const:
            if self.val == other.val:
                return Variable(val=self.val, power=self.power+other.power,
                                const=False, priority=self.priority,
                                asc_desc=self.asc_desc)
            else:
                raise Exception("Cannot not multiply variables of different values")
        else:
            raise Exception

    def __eq__(self, other):
        """
        x.__eq__(y) <==> x == y
        Used for sorting Term printing order
        """

        if self.val == other.val:
            if self.power == other.power:
                return True
        return False

    def __ne__(self, other):
        """
        x.__ne__(y) <==> x != y
        Used for sorting Term printing order
        """

        return not(self == other)

    def __gt__(self, other):
        """
        x.__gt__(y) <==> x > y
        Used for sorting Term printing order
        """

        if self.asc_desc:
            if other.asc_desc:
                if self.priority == other.priority:
                    if self.const and other.const:
                        return int(self.val) > int(other.val)
                    elif other.const:
                        return True
                    elif self.const:
                        return False
                    return self.power > other.power
                else:
                    return self.priority < other.priority
            else:
                return True
        else:
            if other.asc_desc:
                return False
            else:
                if self.priority == other.priority:
                    return self.power < other.power
                else:
                    return self.priority > other.priority

    def __lt__(self, other):
        """
        x.__lt__(y) <==> x < y
        Used for sorting Term printing order
        """

        if self.asc_desc:
            if other.asc_desc:
                if self.priority == other.priority:
                    if self.const and other.const:
                        return int(self.val) < int(other.val)
                    elif other.const:
                        return False
                    elif self.const:
                        return True
                    return self.power < other.power
                else:
                    return self.priority > other.priority
            else:
                return False
        else:
            if other.asc_desc:
                return True
            else:
                if self.priority == other.priority:
                    return self.power > other.power
                else:
                    return self.priority < other.priority

    def __hash__(self):
        """
        x.__hash__() <==> hash(x)
        """

        if self.const:
            return hash("const")
        return hash(self.val)

    def __add__(self, other):
        """
        x.__add__(y) <==> x + y

        Can only be performed in variables of the same 'val'
        """

        if self.const and other.const:
            return Variable(val=str(int(self.val)+int(other.val)))
        else:
            raise Exception("Can only add constant Variables")

    def __sub__(self, other):
        """
        x.__add__(y) <==> x + y

        Can only be performed in variables of the same 'val'
        """

        if self.const and other.const:
            return Variable(val=str(int(self.val)-int(other.val)))
        else:
            raise Exception("Can only subtract constant Variables")



class Term(object):
    """
    Encapsulates a set of variables multiplied together

    ex) 2(x^2)(y^2) is an Term
    """
    def __init__(self, vari):
        self._vari = vari  # vars that make up the term (Variable)
        self._const = Variable()
        if hash(self._const) not in self._vari:
            self._vari[hash(self._const)] = Variable()

    def set_var(self, var):
        """
            Takes a Variable instance and stores in dict.
            Variables are hashed by their 'value', i.e. their symbolic name

            Args:
            var -- Variable instance that is hashed and stored
        """

        self.remove_var(var)
        self._vari[hash(var)] = var

    def var_exists(self, var):
        """
        Returns True if Variable exists in Term

        Args:
        var -- Variable instance

        var_exists(var) -> Bool
        """

        if hash(var) in self._vari:
            return True
        return False

    def is_pos(self):
        """
        Returns True if Term is positive

        is_pos() -> Bool
        """

        return int(self._vari[hash(self._const)].val) > 0

    def get_var(self, var):
        """
        Returns an instance of Variable

        Args:
        var -- Variable instance

        get_var(var) -> Variable
        """

        return self._vari[hash(var)]

    def get_vars(self):
        """
        Returns a dictionary of Variables.
        Dictionary key is an int, value is Variable instance.

        get_vars() -> dict
        """

        return self._vari

    def get_const(self):
        """
        Returns the constant Variable in the Term

        get_const() -> Variable
        """

        return self.get_var(self._const)

    def remove_var(self, var):
        """
        Removes a Variable from the Term

        Args:
        var -- Variable
        """

        if self.var_exists(var):
            del self._vari[hash(var)]

    def __mul__(self, other):
        """
        x.__mul__(y) <==> x * y

        Can multiply a Term by and int or float
        """

        result = Term(deepcopy(self._vari))
        if type(other) == int or type(other) == float:
            temp = int(self.get_var(self._const).val) * other
            result.set_var(Variable(val=str(temp)))
        else:
            for key, val in other.get_vars().iteritems():
                if result.var_exists(val):
                    new_var = other.get_var(val) * result.get_var(val)
                    if new_var.power != 0:
                        result.set_var(new_var)
                    else:
                        result.remove_var(new_var)
                else:
                    result.set_var(val)
        return result

    def __eq__(self, other):  
        """
        x.__eq__(y) <==> x == y
        """

        for elm in self._vari:
            if elm not in other.get_vars():
                return False
            elif self.get_vars()[elm].power != other.get_vars()[elm].power:
                return False
        return True

    def __ne__(self, other): 
        """
        x.__ne__(y) <==> x != y
        """

        return not(self == other)

    def __add__(self, other): 
        """
        x.__add__(y) <==> x + y
        """

        result = Term(deepcopy(self.get_vars()))
        new_var = self.get_const() + other.get_const()
        result.set_var(new_var)
        return result

    def get_priority_vars(self):
        """
        Returns a list of Variables sorted by priority and print order.
        Used for comparing Terms when sorting for print order

        get_priority_vars() -> List
        """

        def get_priority(var):
            return self.get_var(var).priority

        asc_list = []
        desc_list = []
        for key, val in self._vari.iteritems():
            if val.asc_desc:
                asc_list.append(val)
            else:
                desc_list.append(val)
        return sorted(desc_list, key=get_priority) +\
            sorted(asc_list, key=get_priority)

    def __gt__(self, other):   
        """
        x.__gt__(y) <==> x > y
        """

        return self.get_priority_vars() > other.get_priority_vars()

    def __lt__(self, other): 
        """
        x.__lt__(y) <==> x < y
        """

        return self.get_priority_vars() < other.get_priority_vars()

    def __hash__(self): 
        """
        x.__hash__() <==> hash(x)
        """

        hash_str = ""
        for i in self._vari:
            if not self._vari[i].const:
                hash_str += self._vari[i].val
        return hash("".join(sorted(hash_str)))  # order matters for string hash


class Polynomial(object):
    """
    Encapsulates a set of Terms

    ex) (x^2)(y^2) + (z^3)
    """
    def __init__(self, terms):
        self.terms = terms  # dict of termessions that make up the polynomial

    def get_terms(self):
        """
        Returns a dictionary containing Terms for Polynomial

        get_terms() -> dict
        """

        return self.terms
    
    def set_term(self, term):
        """
        Removes an equivalent terms if it exists, and sets the new one.

        Args:
        term -- Term
        """

        self.remove_term(term)
        self.terms[term] = term

    def get_term(self, term):
        """
        Returns an equivalent Term if it exists, returns None otherwise

        Args:
        term -- Term

        get_term(term) -> Term
        """

        if self.term_exists(term):
            return self.terms[term]
        return None

    def term_exists(self, term):
        """
        Returns True if the Term exists

        Args:
        term -- Term

        term_exists(term) -> Bool
        """

        return term in self.terms

    def remove_term(self, term):
        """
        Removes the Term if it exists

        Args:
        term -- Term
        """

        if self.term_exists(term):
            del self.terms[term]

    def add_term(self, term):
        """
        If the Term exists, the term is updated with the sum.
        Sets the Term if it does not exist

        Args:
        term -- Term
        """

        if self.term_exists(term):
            temp = term + self.terms[term]
            if int(temp.get_const().val) == 0:
                self.remove_term(temp)
            else:
                self.set_term(temp)
        else:
            self.set_term(term)

    def __mul__(self, other):
        """
        x.__mul__(y) <==> x * y
        """

        result = Polynomial({})
        if type(other) == int or type(other) == float:
            for term in self.terms:
                result.add_term(self.terms[term] * other)
        else:
            for pexr in self.terms:
                for sexr in other.get_terms():
                    temp = sexr*pexr
                    result.add_term(temp)
        return result

    @staticmethod
    def generate_poly():
        """
        Returns a Polynomial equivalent to '1'

        generate_poly() -> Polynomial
        """

        term = Term({})
        poly = Polynomial({term: term})
        return poly

    def pretty_print(self):
        """
        Returns a two element list that contains the top and bottom for print.
        Assumes descending order trumps ascending order.
        [top, bottom]

        pretty_print() -> List
        """

        def var_cmp(x, y):
            # cmp used for sorting Variables in Term
            if x.const:
                return 1
            elif y.const:
                return -1
            elif x.power == y.power:
                return 0
            elif x.power > y.power:
                return 1
            else:
                return -1

        exp_str = ""
        var_str = ""
        space = " "
        minus = "-"
        plus = "+"
        sort_term = sorted(self.terms)
        first_term = min(sort_term)
        first = True
        if not first_term.is_pos():
            var_str += minus
            exp_str += space

        for term in sort_term:
            if first:
                first = False
            else:
                if term.is_pos():
                    var_str += plus + space
                else:
                    var_str += minus + space
                exp_str += space*2
            cur_terms = term.get_vars()
            for val in sorted(cur_terms, key=cur_terms.get, cmp=var_cmp, reverse=True):
                var = cur_terms[val]
                if not var.const:
                    if abs(var.power) > 1:
                        exp_str += space + str(var.power)
                        var_str += var.val + space*len(str(var.power))
                    else:
                        exp_str += space
                        var_str += var.val
                else:
                    if len(term.get_vars()) > 1:
                        if abs(int(var.val)) > 1:
                            exp_str += space*len(var.val)
                            var_str += str(abs(int(var.val)))
                    else:
                        exp_str += space*len(var.val)
                        var_str += str(abs(int(var.val)))
            exp_str += space
            var_str += space

        return [exp_str, var_str]


class PolynomialParser(object):
    def __init__(self, pstring=""):
        self.pstring = pstring
        self.poly = Polynomial({})
        self.current_vars = []
        self.current_const = ""
        self.vp = {'x': [1, False],  # acceptable vars, with print ordering
                   'y': [1, True]}  # [priority, asc_desc]

    def _symbol(self, symbol):
        """
        Accepts a string which is assumed to be a arithmetic symbol.
        Generates a new Term for the result Polynomial

        Args:
        symbol -- String
        """

        if self.current_const != "":
            if len(self.current_vars) == 1:  # Is a coefficient
                self.current_vars[0].val = str(int(self.current_vars[0].val) *
                                               int(self.current_const))
            else:  # Is an exponent
                self.current_vars[-1].power = int(self.current_const)
            self.current_const = ""

        if len(self.current_vars) > 0:
            current_term = Term({})
            while len(self.current_vars) > 0:
                current_term.set_var(self.current_vars.pop())
            self.poly.add_term(current_term)
        current_var = Variable(val=symbol+"1")
        self.current_vars.append(current_var)

    def _var(self, var):
        """
        Accepts a string which is assumed to be alphanumeric.
        Generates a new Variable for the current Term.
        Alphabetic characters are restricted to what's defined to self.vp.

        Args:
        var -- String
        """

        if var.isdigit():
            self.current_const += var
        else:
            if self.current_const != "":
                if len(self.current_vars) == 1:  # Is a coefficient
                    self.current_vars[0].val = str(int(self.current_vars[0].val) *
                                                   int(self.current_const))
                else:  # Is an exponent
                    self.current_vars[-1].power = int(self.current_const)
                self.current_const = ""
            temp = Variable(val=var, const=False, priority=self.vp[var][0],
                            asc_desc=self.vp[var][1])
            self.current_vars.append(temp)
            
    def parse(self):
        """
        Parses the Polynomial string.
        Returns a Polynomial object.

        parse() -> Polynomial
        """

        if self.pstring[0] != "-":
            self.current_vars.append(Variable())
        for elm in self.pstring:
            if elm.isalnum():
                self._var(elm)
            else:
                self._symbol(elm)
        self._symbol("+")
        del self.current_vars[0]  # hacky
        return self.poly


def main():
    number_poly = 2  # number of polynomials to multiply
    stop_char = "#"
    polys = []
    parsers = []
    current_poly = Polynomial.generate_poly()
    count = 1
    lines = []
    with open('input.txt', 'r') as f:
        lines = [l.strip() for l in f.readlines()]

    for line in lines:
        if line == stop_char:
            break
        parsers.append(PolynomialParser(line)) 
        line_poly = parsers[-1].parse()
        polys.append(line_poly)

    for poly in polys:
        current_poly = poly * current_poly
        if count >= number_poly:
            top, bottom = current_poly.pretty_print()
            print top
            print bottom
            count = 0
            current_poly = Polynomial.generate_poly()
        count += 1

    if count != 1:
        top, bottom = current_poly.pretty_print()
        print top
        print bottom

if __name__ == "__main__":
    main()
