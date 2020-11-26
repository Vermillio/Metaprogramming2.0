Keywords = ['as', 'class', 'break',	'continue',	'do', 'else',
'for', 'fun', 'false', 'if', 'in', 'interface',
'super', 'return', 'object', 'package',	'null',	'is',
'try', 'throw', 'true', 'this', 'typeof', 'typealias',
'when',	'while', 'val',	'var']

Operators = [
'+', '-', '*', '/', '%', '=',
'+=', '-=', '*=', '/=', '%=',
'++', '--',
'&&', '||', '!',
'==', '!=',
'===', '!==',
'<', '>', '<=', '>='
'[', ']', '!!', '?.', '?:', '::', '..', ':', '?', '->', '@', ';', '$', '_'
]

Punctuators = [';', ':', ',', '.', '(', ')', '[', ']', '{', '}']

def isMultilineCommentStart(str):
    return str.startswith('/*')

def isMultilineCommentEnd(str):
    return str.startswith('*/')

def isMultilineComment(str):
    if DebugRecognizerNames:
        print("isMultilineComment")
    if isMultilineCommentStart(str):
        pos=2
        while pos < len(str) and not isMultilineCommentEnd(str[pos:]):
            pos+=1
        if pos < len(str)-2 and isMultilineCommentEnd(str[pos:]):
            return pos+2, "CommentMultiline", str[:pos+2]
        return pos, "UnfinishedComment", str
    return 0, None, None

def isCommentStart(str):
    return str.startswith('//')

def isLineEnd(str):
    return str[0] == '\n'

def isComment(str):
    if DebugRecognizerNames:
        print("isComment")
    if isCommentStart(str):
        pos=2
        while pos < len(str):
            if isLineEnd(str[pos:]):
                return pos, "Comment", str[:pos]
            pos+=1
        return len(str), "Comment", str
    return 0, None, None

def isWhiteSpace(str):
    if DebugRecognizerNames:
        print("isWhiteSpace")

    if str[0] == '\n':
        return 1, "Newline", str[:1]
    if str[0] == ' ':
        return 1, "Whitespace", str[:1]
    if str[0]=='\t':
        return 1, "Whitespace", str[:1]
    if str[0] in string.whitespace:
        return 1, "Whitespace", str[:1]
    return 0, None, None

def isPunctuator(str):
    if DebugRecognizerNames:
        print("isPunctuator")
    if str[0] in Punctuators:
        return 1, "Punctuator", str[:1]
    else:
        return 0, None, None

def isIdentifier(str):
    if DebugRecognizerNames:
        print("isIdentifier")
    if str[0].isalpha() or str[0]=='_':
        pos = 0
        while pos < len(str) and (str[pos].isalpha() or str[pos].isdigit() or str[pos]=='_'):
            pos+=1
        return pos, "Identifier", str[:pos]
    return 0, None, None

def isKeyword(str):
    if DebugRecognizerNames:
        print("isKeyword")
    for k in Keywords:
        if str.startswith(k):
            if len(k) >= len(str) or (not str[len(k)].isalnum() and not str[len(k)] in ['_']):
                return len(k), "Keyword", str[:len(k)]
    return 0, None, None

def isOperator(str):
    if DebugRecognizerNames:
        print("isOperator")
    opers = [op for op in Operators if str.startswith(op)]
    opers.sort(key=lambda a: -len(a))
    if len(opers):
        return len(opers[0]), "Operator", str[:len(opers[0])]
    else:
        return 0, None, None

def isNullLiteral(str):
    if DebugRecognizerNames:
        print("isNullLiteral")
    if len(str) >= 3 and str.startswith('null'):
        if len(str) == 3 or (not str[4].isalnum() and not str[4] in ['_']):
            return 4, "Literal", str[:4]
    return 0, None, None

def isBooleanLiteral(str):
    if DebugRecognizerNames:
        print("isBooleanLiteral")
    if len(str) >= 4 and str.startswith('true'):
        if len(str) == 4 or (not str[5].isalnum() and not str[5] in ['_']):
            return 5, "Literal", str[:5]
    if len(str) >= 5 and str.startswith('false'):
        if len(str) == 5 or (not str[6].isalnum() and not str[6] in ['_']):
            return 6, "Literal", str[:6]
    return 0, None, None

def isCharacterLiteral(str):
    if DebugRecognizerNames:
        print("isCharacterLiteral")
    if (len(str) >= 7 and str[0]=='\''
       and ( str[1]=='u' or str[1]=='x' )
       and (str[2].isdigit() and str[3].isidigit() and str[4].isdigit() and str[5].isdigit())
       and str[6] == '\''):
        return 7, "Literal", str[:7]
    if len(str) >= 4 and str[0]=='\'' and str[1]=='\\' and str[3]=='\'':
        return 4, "Literal", str[:4]
    if len(str) >= 3 and str[0]=='\'' and str[2]=='\'':
        return 3, "Literal", str[:3]
    return 0, None, None

def isStringLiteral(str):
    if DebugRecognizerNames:
        print("isStringLiteral")
    # todo: String Interpolation
    if len(str) >= 2:
        pos = 0
        Interpolation = False
        if str[pos]=='$':
            pos+=1
            Interpolation=True
        if str[pos] == '"':
            if len(str) > = 6:
                if str[pos+1] == '"' and str[pos+2] == '"':
                    # multiline string
                    pos+=3
                    while pos < len(str) - 2:
                        if str[pos] == '"' and str[pos+1] == '"' and str[pos+2] == '"':
                            return pos+3, "Literal", str[:pos+3]
                        pos+=1
                    return pos+2, "Literal", str
            while pos < len(str):
                if pos + 1 < len(str):
                    if (not str[pos]=='\\' and str[pos+1]=='"'):
                        return pos+2, "Literal", str[:pos+2]
                pos += 1
    return 0, None, None

class DecLiteralFSM(FiniteStateMachine):

    pos = 0

    def __init__(self):
        super().__init__()
        self.add_state('s0', self.s0_handler)
        self.add_state('s1', self.s1_handler)
        self.add_state('s2', self.s2_handler)
        self.add_state('s3', self.s3_handler)
        self.add_state('s4', self.s4_handler)
        self.add_state('s5', self.s5_handler)
        self.add_state('s6', self.s6_handler)
        self.add_state('passed', self.passed_handler, True)
        self.add_state('exit_state', self.exit_handler, True)
        self.set_start('s0')

    def run(self, input):
        return super().run(input), self.pos

    def s0_handler(self, str):
        if str[self.pos].isdigit():
            self.pos+=1
            return 's1', str
        return 'exit_state', str

    def s1_handler(self, str):
        if str[self.pos].isdigit():
            self.pos+=1
            return 's1', str
        if str[self.pos] == '.':
            self.pos+=1
            return 's2', str
        if str[self.pos] == 'E' or str[self.pos] == 'e':
            self.pos+=1
            return 's4', str
        return 'passed', str

    def s2_handler(self, str):
        if str[self.pos].isdigit():
            self.pos+=1
            return 's3', str
        return 's3', str

    def s3_handler(self, str):
        if str[self.pos].isdigit():
            self.pos+=1
            return 's3', str
        if str[self.pos] in ['L', 'f', 'F']:
            self.pos+=1
            return 'passed', str
        if str[self.pos] == 'E' or str[self.pos] == 'e':
            self.pos+=1
            return 's4', str
        return 'exit_state', str

    def s4_handler(self, str):
        if str[self.pos] == '+' or str[self.pos] == '-':
            self.pos+=1
            return 's5', str
        if str[self.pos].isdigit():
            self.pos+=1
            return 's6', str
        return 'exit_state', str

    def s5_handler(self, str):
        if str[self.pos].isdigit():
            self.pos+=1
            return 's6', str
        return 'exit_state', str

    def s6_handler(self, str):
        if str[self.pos].isdigit():
            self.pos+=1
            return 's6', str
        return 'passed', str

    def passed_handler(self, str):
        return None, str
    def exit_handler(self, str):
        return None, str

class HexLiteralFSM(FiniteStateMachine):

    pos=0

    def __init__(self):
        super().__init__()
        self.add_state('s0', self.s0_handler)
        self.add_state('s1', self.s1_handler)
        self.add_state('s2', self.s2_handler)
        self.add_state('s3', self.s3_handler)
        self.add_state('passed', self.passed_handler, True)
        self.add_state('exit_state', self.exit_handler, True)
        self.set_start('s0')

    def run(self, input):
        return super().run(input), self.pos

    def s0_handler(self, str):
        if str[self.pos] == '0':
            self.pos+=1
            return 's1', str
        return 'exit_state', str

    def s1_handler(self, str):
        if str[self.pos] == 'x':
            self.pos+=1
            return 's2', str
        return 'exit_state', str

    def s2_handler(self, str):
        if str[self.pos].isdigit() or str[self.pos] in ['A', 'B', 'C', 'D', 'E', 'F']:
            self.pos+=1
            return 's3', str
        return 'exit_state', str

    def s3_handler(self, str):
        if str[self.pos].isdigit() or str[self.pos] in ['A', 'B', 'C', 'D', 'E', 'F']:
            self.pos+=1
            return 's3', str
        return 'passed', str

    def passed_handler(self, str):
        return None, str
    def exit_handler(self, str):
        return None, str

class BinLiteralFSM(FiniteStateMachine):

    pos=0

    def __init__(self):
        super().__init__()
        self.add_state('s0', self.s0_handler)
        self.add_state('s1', self.s1_handler)
        self.add_state('s2', self.s2_handler)
        self.add_state('s3', self.s3_handler)
        self.add_state('passed', self.passed_handler, True)
        self.add_state('exit_state', self.exit_handler, True)
        self.set_start('s0')

    def run(self, input):
        return super().run(input), self.pos

    def s0_handler(self, str):
        if str[self.pos] == '0':
            self.pos+=1
            return 's1', str
        return 'exit_state', str

    def s1_handler(self, str):
        if str[self.pos] == 'b':
            self.pos+=1
            return 's2', str
        return 'exit_state', str

    def s2_handler(self, str):
        if str[self.pos] in ['0', '1']:
            self.pos+=1
            return 's3', str
        return 'exit_state', str

    def s3_handler(self, str):
        if str[self.pos] in ['0', '1']:
            self.pos+=1
            return 's3', str
        return 'passed', str

    def passed_handler(self, str):
        return None, str
    def exit_handler(self, str):
        return None, str

def isNumericLiteral(str):
    if DebugRecognizerNames:
        print("isNumericLiteral")
    fsm = DecLiteralFSM()
    state, pos = fsm.run(str)
    if state == 'passed':
        return pos, "Literal", str[:pos]
    fsm = HexLiteralFSM()
    state, pos = fsm.run(str)
    if state == 'passed':
        return pos, "Literal", str[:pos]
    fsm = BinLiteralFSM()
    state, pos = fsm.run(str)
    if state == 'passed':
        return pos, "Literal", str[:pos]

    return 0, None, None


def countNewlines(str):
    counter=0
    for s in str:
        if s=='\n':
            counter+=1
    return counter


class KotlinLexer:

    pos=0
    line=0

    recognizers = [ isWhiteSpace,
                    isComment,
                    isMultilineComment,
                    isKeyword,
                    isIdentifier,
                    isPunctuator,
                    isOperator,
                    isNullLiteral,
                    isBooleanLiteral,
                    isStringLiteral,
                    isCharacterLiteral,
                    isNumericLiteral,
                    isPreprocessorDirective, ]

    def __init__(self, str):
        self.str = str
        self.reset()


    def nextToken(self):
        if self.pos >= len(self.str):
            return "EndOfInput", ""
        if set(self.str[self.pos]).difference(string.printable):
            print("Deleted character " + self.str[self.pos])
            self.pos+=1
        if self.pos >= len(self.str):
            return "EndOfInput", ""
        for recognizer in self.recognizers:
            delta_pos, token_type, value = recognizer(self.str[self.pos:])
            if delta_pos != 0:
                line+=countNewlines(self.str[self.pos:self.pos+delta_pos])
                self.pos += delta_pos
                return token_type, value, line
        print(self.str[self.pos])
        return Error, ""

    def reset(self):
        self.pos = 0
        self.line = 0
