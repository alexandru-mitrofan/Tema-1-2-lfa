from typing import Callable, Generic, TypeVar
import sys
S = TypeVar("S")
T = TypeVar("T")

nfa_creator = []
class Op1El:
    def __init__(self, name, a):
        self.name = name
        self.a = a

    def __radd__(self, other):
        return other + str(self)
    
    def __str__(self):
        if self.a is not None:
            return self.name + "(" + self.a + ")"
        else:
            return self.name + "(?)"


        
class Op2El(Op1El):

    def __init__(self, name, a, b):
        self.name = name
        self.a = a
        self.b = b

    def __str__(self):
        if self.a is not None and self.b is not None:
            return self.name + "(" + self.a + "," + self.b + ")"
        elif self.a is not None and self.b is None:
            return self.name + "(" + self.a + ",?)"
        elif self.a is not None and self.b is None:
            return self.name + "(?," + self.b + ")"
        else:
            return self.name + "(?,?)"

numberOfState = -1

class State:
    def __init__(self, val):
        if str(val) == "":
            self.state = None
        self.state = str(val)

    def __hash__(self):
        return hash(self.state)
    
    def __eq__(self, other):
        return self.state == other.state
    
    def __repr__(self):
        return "<%s>" % self.state

    def __lt__(self, other):
        return self.state < other.state

    def __str__(self):
        return self.state
		



class NFA(Generic[S]):
	
	def __init__(self):
		self.finalState = None
		self.initialState = None
		self.delta = dict()
		self.states = set()
		self.alphabet = set()
		
	def map(self, f: Callable[[S], T]) -> 'NFA[T]':
		return NFA()

	def next(self, from_state: S, on_chr: str) -> 'set[S]':
		pass

	def getStates(self) -> 'set[S]':
		pass

	def accepts(self, str: str) -> bool:	
		return doaccepts(self,str,self.initialState)


	def isFinal(self, state: S) -> bool:
		pass

	@staticmethod
	def fromPrenex(str: str) -> 'NFA[int]':
		global nfa_creator
		global numberOfState
		global good_nfa
		good_nfa = NFA()
		stv = []
		nfa_creator = []
		numberOfState = -1
		operators = ["CONCAT", "STAR", "UNION", "PLUS", "MAYBE"]
		contor = 0
		for i in str:
			if i == "'":
				contor = contor + 1
		if contor % 2 == 0:
			str = str.replace("'","")
		else:
			str = str.replace("'","",contor - 1)
		if str != ' ' and str !='\r' and str != '\n' and str != '	':
			regex = str.split()
		else:
			regex = str
		final_regex = ""
		for x in regex:
			if x in operators:
				if x == "STAR" or x == "PLUS" or x == "MAYBE":
					stv.append(Op1El(x, None)) 
				else:
					stv.append(Op2El(x, None, None))
			else:
				good_nfa.alphabet.add(x)
				if stv:
					while stv:
						el = stv.pop()
						if isinstance(el, Op2El):
							if el.a is None:
								el.a = x
								stv.append(el)
								break
							el.b = x
						elif isinstance(el, Op1El):
							el.a = x
						x = el
						final_regex = el
				else:
					final_regex = x
					stv.append(x)
		
		create_nfa(final_regex)
		good_nfa.delta = nfa_creator[0].delta

		for i in good_nfa.delta:

			good_nfa.states.add(i)
			for j in good_nfa.delta[i]:
				for k in j[1]:
					good_nfa.states.add(k)
		good_nfa.initialState = nfa_creator[0].initialState
		good_nfa.finalState = nfa_creator[0].finalState
		return good_nfa



def atom(char):
    global nfa_creator
    global numberOfState
    nfa_helper = NFA()
    numberOfState += 1
    nfa_helper.initialState = State(numberOfState)
    numberOfState += 1
    nfa_helper.finalState = State(numberOfState)
    nfa_helper.delta = {nfa_helper.initialState: [(char, [nfa_helper.finalState])]}
    nfa_creator.append(nfa_helper)



def concat():
    global nfa_creator
    global numberOfState
    nfa_helper = NFA()
    first_nfa = nfa_creator.pop()
    second_nfa = nfa_creator.pop()
    nfa_helper.initialState = State(second_nfa.initialState)
    nfa_helper.finalState = State(first_nfa.finalState)
    nfa_helper.delta.update(second_nfa.delta)
    nfa_helper.delta.update(first_nfa.delta)
    nfa_helper.delta[second_nfa.finalState] = [('eps', [first_nfa.initialState])]
    nfa_creator.append(nfa_helper)
    
def maybe():
    global nfa_creator
    global numberOfState
    nfa_helper = NFA()
    first_nfa = nfa_creator.pop()
    numberOfState += 1
    nfa_helper.initialState = State(numberOfState)
    numberOfState += 1
    nfa_helper.finalState = State(numberOfState)
    nfa_helper.delta = first_nfa.delta
    nfa_helper.delta[nfa_helper.initialState] = [('eps', [first_nfa.initialState, nfa_helper.finalState])]
    nfa_helper.delta[first_nfa.finalState] = [('eps', [nfa_helper.finalState])]
    nfa_creator.append(nfa_helper)

def union():
    global nfa_creator
    global numberOfState
    nfa_helper = NFA()
    first_nfa = nfa_creator.pop()
    second_nfa = nfa_creator.pop()
    numberOfState += 1
    nfa_helper.initialState = State(numberOfState)
    numberOfState += 1
    nfa_helper.finalState = State(numberOfState)
    nfa_helper.delta.update(first_nfa.delta)
    nfa_helper.delta.update(second_nfa.delta)
    nfa_helper.delta[nfa_helper.initialState] = [('eps', [first_nfa.initialState, second_nfa.initialState])]
    nfa_helper.delta[first_nfa.finalState] = [('eps', [nfa_helper.finalState])]
    nfa_helper.delta[second_nfa.finalState] = [('eps', [nfa_helper.finalState])]
    nfa_creator.append(nfa_helper)


def star():
    global nfa_creator
    global numberOfState
    nfa_helper = NFA()
    first_nfa = nfa_creator.pop()
    numberOfState += 1
    nfa_helper.initialState = State(numberOfState)
    numberOfState += 1
    nfa_helper.finalState = State(numberOfState)
    nfa_helper.delta = first_nfa.delta
    nfa_helper.delta[nfa_helper.initialState] = [('eps', [first_nfa.initialState, nfa_helper.finalState])]
    nfa_helper.delta[first_nfa.finalState] = [('eps', [first_nfa.initialState, nfa_helper.finalState])]
    nfa_creator.append(nfa_helper)


def plus():
    global nfa_creator
    global numberOfState
    nfa_helper = NFA()
    first_nfa = nfa_creator.pop()
    numberOfState += 1
    nfa_helper.initialState = State(numberOfState)
    numberOfState += 1
    nfa_helper.finalState = State(numberOfState)
    nfa_helper.delta = first_nfa.delta
    nfa_helper.delta[nfa_helper.initialState] = [('eps', [first_nfa.initialState])]
    nfa_helper.delta[first_nfa.finalState] = [('eps', [first_nfa.initialState, nfa_helper.finalState])]
    nfa_creator.append(nfa_helper)


def create_nfa(regex):
    if isinstance(regex, Op1El) or isinstance(regex, Op2El):
        if regex.name == "UNION":
            create_nfa(regex.a)
            create_nfa(regex.b)
            union()
        if regex.name == "STAR":
            create_nfa(regex.a)
            star()
        if regex.name == "CONCAT":
            create_nfa(regex.a)
            create_nfa(regex.b)
            concat()
        if regex.name == "PLUS":
            create_nfa(regex.a)
            plus()
        if regex.name == "MAYBE":
            create_nfa(regex.a)
            maybe()
        return
    atom(regex)

def doaccepts(nfa , string ,currstate):
	if currstate == nfa.finalState and len(string) == 0:
		return True
	preca = False

	if currstate != nfa.finalState:
		lista = nfa.delta[currstate]
		if len(string) == 0 and lista[0][0] != "eps":
			return False
		if len(string)!=0:
			if string[0] == lista[0][0]:
				for i in lista[0][1]:
					a = doaccepts(nfa,string[1:],i)
					preca = a or preca
		if lista[0][0] == "eps":
			for i in lista[0][1]:
				a = doaccepts(nfa,string,i)
				preca = a or preca
        
		
	return preca
def makestr(regex):
	return str(regex)

good_nfa = NFA()
