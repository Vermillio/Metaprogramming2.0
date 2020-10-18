class FSMState:
    def __init__(self, tokenType):
        self.tokenType = tokenType

    def isEndState(self):
        return not self.tokenType == None

class FSMHandler:

    def __init__(self, states, transitions, defaultState):
        # states - array, transitions - array of array of strings
        self.transitions=transitions
        self.states=states
        self.defaultState=defaultState

    def __call__(self, str):
        for i, transition in enumerate(transitions):
            result = transition(str)
            if result:
                return states[i], result
        return defaultState, str[1:]

class FiniteStateMachine:
    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.endStates = []

    def add_state(self, name, handler, end_state=0):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    def set_start(self, name):
        self.startState = name.upper()

    def run(self, input):
        try:
            handler = self.handlers[self.startState]
        except:
            raise InitializationError("must call .set_start() before .run()")
        if not self.endStates:
            raise  InitializationError("at least one state must be an end_state")

        while True:
            (newState, input) = handler(input)
            if newState.upper() in self.endStates:
                return newState
            else:
                handler = self.handlers[newState.upper()]
