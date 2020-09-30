import FiniteStateMachine
import Tokens

Token = TokenType()

Comment = Token.Comment
Keyword = Token.Keyword
Identifier = Token.Identifier
Literal = Token.Literal
Operator = Token.Operator
Punctuator = Token.Punctuator

CommentMultiline = Comment.CommentMultiline

NumericLiteral = Literal.NumericLiteral
CharacterLiteral = Literal.CharacterLiteral
BooleanLiteral = Literal.BooleanLiteral
StringLiteral = CharacterLiteral.StringLiteral
IntegerLiteral = NumericLiteral.IntegerLiteral


Handlers = Map()

EndStates = [
    # FSMState(Token.Comment),
    # FSMState(Token.CommentMultiline),
    # FSMState(Token.Keyword),
    # FSMState(Token.Literal)
]


# C# Language Definitions

ArithmeticOperators = ['+','-','*','/','%']
LogicalOperators = ['||', '&&', '!']
RelationalOperators = ['>=', '<=', '==', '!=', '<', '>']
AssignmentOperators = ['+=', '-=', '=']
BitwiseOperators = ['&', '|', '~', '^', '>>', '<<']
IncrementOperators=['++', '--']
SpecialOperators=['is', 'sizeof', 'as', 'typeof', 'new', 'checked', 'unchecked', 'dot']

# TERNARY OPERATOR

Operators = ArithmeticOperators + LogicalOperators + RelationalOperators + AssignmentOperators + BitwiseOperators + IncrementOperators + SpecialOperators

Punctuators = [';', ':', ',', '.', '(', ')', '[', ']', '{', '}']



def isCommentStarted(str):
    return str[2:] if str.startswith('/*') else None

def isCommentEnded(str):
    return str[2:] if str.startswith('*/') else None

def isLineEnded(str):
    return str[1:] if str[0] == '\n' else None

def isOperator(str):
    opers = [op for op in Operators if str.startswith(op)]
    opers.sort(key=lambda a: -len(a))
    return str[len(opers[0]):] if len(opers) else None

def isPunctuator(str):
    return 1, Token.Punctuator, str[:1] if str[0] in Punctuators else 0, None, None

def isIdentifier(str):
    if isalpha(str[0]):
        pos = 0
        while pos < len(str) and not isspace(str[pos]):
            pos+=1
        return pos, Token.Identifier, str[:pos]
    return 0, None, None


# states_to_tokens = {}
# states_to_tokens['s3'] = Token.Operator
# states_to_tokens['comment_state'] = Token.Comment
#
# Handlers={}
# Handlers['start_state'] = FSMHandler([('s2', isCommentStarted), ('s3', isOperator), ('s4', is)], 'start_state')
# Handlers['s2'] = FSMHandler([('comment_state',isLineEnded), 's2')
# Handlers['s4'] = FSMHandler([(),()])


def s0_handler(str):
    if isdigit(str[pos]):
        return 's1', str[1:]
    return 'exit_state', str

def s1_handler(str):
    if isdigit(str[0]):
        return 's1', str[1:]
    if str[0] == '.':
        return 's2', str[1:]
    if str[0] == 'E' or str[0] == 'e':
        return 's4', str[1:]
    return 'exit_state', str

def s2_handler(str):
    if isdigit(str[0]):
        return 's3', str[1:]
    return 'exit_state', str

def s3_handler(str):
    if isdigit(str[0]):
        return 's3', str[1:]
    if str[0] == 'E' or str[0] == 'e':
        return 's4', str[1:]
    return 'exit_state', str

def s4_handler(str):
    if str[0] == '+' or str[0] == '-':
        return 's5', str[1:]
    if isdigit(str[0]):
        return 's6', str[1:]
    return 'exit_state', str

def s5_handler(str):
    if isdigit(str[0]):
        return 's6', str[1:]
    return 'exit_state', str

def s6_handler(str):
    if isdigit(str[0]):
        return 's6', str[1:]
    return 's7', str[1:]

def s7_handler(str):
    return None, str

def exit_handler(str):
    return None, str

NumericLiteralFSM = FiniteStateMachine()
NumericLiteralFSM.add_state('s0', s0_handler)
NumericLiteralFSM.add_state('s1', s1_handler)
NumericLiteralFSM.add_state('s2', s2_handler)
NumericLiteralFSM.add_state('s3', s3_handler)
NumericLiteralFSM.add_state('s4', s4_handler)
NumericLiteralFSM.add_state('s5', s5_handler)
NumericLiteralFSM.add_state('s6', s6_handler)
NumericLiteralFSM.add_state('s7', s7_handler, True)
NumericLiteralFSM.add_state('exit_state', exit_handler, True)

def isNumericLiteral(str):
    state = NumericLiteralFSM.run(str)
    return true if state == 's7' else false


def isLiteral(str):
    
    pass


class CSharpLexer:

    # fsm = FiniteStateMachine()

    recognizers = [isIdentifier, isPunctuator, isOperator]

    def __init__(self, input):
        self.input = input
        self.position = 0
        # fsm.add_state()

    def nextToken(self):
        if pos >= len(str):
            return Token.EndOfInput, ""
        for recognizer in recognizers:
            delta_pos, token_type, value = recognizer(str[pos:])
            if delta_pos != 0:
                pos += delta_pos
                return token_type, value
        return Token.Error, ""



    # def tokenize(self, str):
    #     state = StateMachine.run(str)
    #     return state.tokenType
