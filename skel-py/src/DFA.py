from typing import Callable, Generic, TypeVar
import NFA

S = TypeVar("S")
T = TypeVar("T")
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
        return "%s" % self.state

    def __lt__(self, other):
        return self.state < other.state

    def __str__(self):
        return self.state

class DFA(Generic[S]):
	def __init__(self):
		self.finalStates = set()
		self.initialState = None
		self.delta = dict()
		self.states = set()
		self.alphabet = set()
    
	def map(self, f: Callable[[S], T]) -> 'DFA[T]':
		pass

	def next(self, from_state: S, on_chr: str) -> S:
		pass

	def getStates(self) -> 'set[S]':
		pass

	def accepts(self, str: str) -> bool:
		return doaccepts(self,str,self.initialState)

	def isFinal(self, state: S) -> bool:
		pass

	@staticmethod
	def fromPrenex(str: str) -> 'DFA[int]':
		global good_nfa
		global good_dfa
		good_dfa = DFA()
		good_nfa = NFA.NFA()
		good_nfa = NFA.NFA.fromPrenex(str)
		transform_nfa_in_dfa()
		good_nfa.finalState.final = True
		return good_dfa



def make_states_good():
    global good_nfa
    global good_dfa
    new_delta = dict()
    states_help = good_dfa.states.copy()
    s = set()
    new_states = dict()
    l = len(good_dfa.states)
    new_final_states = set()

    for i in range(l):
        q = states_help.pop()
        new_states[q] = i
        s.add(i)
        if q in good_dfa.finalStates:
            new_final_states.add(i)
    good_dfa.finalStates = new_final_states
    good_dfa.states = s

    for i in good_dfa.delta:
        new_delta[new_states[i]] = {}
        for j in good_dfa.delta[i]:
            new_delta[new_states[i]].update({j: new_states[good_dfa.delta[i][j]]})

    good_dfa.delta = new_delta
    good_dfa.initialState = new_states[good_dfa.initialState]
    
def close_eps(state, eps):
    global good_nfa
    global good_dfa
    notmanaged = set()
    eps[state] = {state}
    if state in good_nfa.delta:
        notmanaged.add(state)
    managed = set()
    while notmanaged:
        current_state = notmanaged.pop()
        managed.add(current_state)
        if current_state in good_nfa.delta:
            for i in good_nfa.delta[current_state]:
                if i[0] == 'eps':
                    for j in i[1]:
                        if j not in managed:
                            eps[state].add(j)
                            notmanaged.add(j)


def sink():
    global good_nfa
    global good_dfa
    sink = State(len(good_nfa.states))
    good_dfa.delta[sink] = {}
    good_dfa.states.add(sink)

    for state in good_dfa.states:
        for atom in good_dfa.alphabet:
            if atom not in good_dfa.delta[state]:
                good_dfa.delta[state].update({atom: sink})

def transform_nfa_in_dfa():
    global good_nfa
    global good_dfa
    eps = dict()
    for state in good_nfa.states:
        close_eps(state, eps)
   
    initial_state = ""
    for i in (eps[good_nfa.initialState]):
        initial_state += " " + str(i)
    good_dfa.initialState = State(initial_state[1:])
    notmanaged = set()
    managed = set()
    notmanaged.add(good_dfa.initialState)
    good_dfa.alphabet.update(good_nfa.alphabet)
    while notmanaged:
        eps_state = notmanaged.pop()
        managed.add(eps_state)
        if eps_state not in good_dfa.states:
            good_dfa.states.add(eps_state)
        states = str(eps_state).split(" ")
        transitions = dict()
        current_trans = []
        
        for state in states:
            if State(state) in good_nfa.delta:
                current_trans = good_nfa.delta[State(state)]
            if State(state) == good_nfa.finalState:
                good_dfa.finalStates.add(eps_state)
            for i in current_trans:
                if i[0] != 'eps':
                    aux_transitions = set(transitions[i[0]]) if i[0] in transitions else set()
                    for j in i[1]:
                        aux_transitions.update(eps[j])
                        aux_transitions.add(j)
                    transitions[i[0]] = aux_transitions
                    

        for i in transitions:
            set_state = transitions[i]
            new_state = ""
            for j in set_state:
                new_state += " " + str(j)
            new_state = State(new_state[1:])
            if new_state not in managed:
                notmanaged.add(new_state)
            transitions[i] = new_state
        
        good_dfa.delta[eps_state] = transitions
    
    sink()
    make_states_good()



def doaccepts(dfa , string ,currstate):
	flag = False
	for i in dfa.finalStates:
		if(currstate == i): 
			flag = True	
	if len(string) == 0 and flag == True :
		return True
	if len(string) == 0 and flag == False:
		return False
	if string[0] == "@":
		string = "?" + string[1:] 
	if string[0] == " " and "@" in dfa.alphabet:
		string = "@" + string[1:] 
	if(string[0] in dfa.alphabet ):
		return doaccepts(dfa,string[1:],dfa.delta[currstate][string[0]])
	else:
		return False
good_nfa = NFA.NFA()
good_dfa = DFA()

s = "CONCAT UNION a b c"
print(DFA.fromPrenex(s).accepts("ac"))