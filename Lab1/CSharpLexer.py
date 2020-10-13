from FiniteStateMachine import *

from CSharpLangDefs import *

DebugRecognizerNames = False

# RECOGNITION FUNCTIONS

# todo:
# ternary operator

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
        if pos < len(str)-1 and isMultilineCommentEnd(str[pos:]):
            return pos+2, Token.CommentMultiline, str[:pos+2]
        return pos, Token.UnfinishedComment, str
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
                return pos+1, Token.Comment, str[:pos+1]
            pos+=1
    return 0, None, None

def isWhiteSpace(str):
    if DebugRecognizerNames:
        print("isWhiteSpace")
    pos = 0
    if str[pos] == '\n':
        return pos+1, Token.NewLine, str[:pos]
    while pos < len(str):
        if not str[pos].isspace() or str[pos] == '\n':
            break
        pos+=1
    if pos == 0:
        return 0, None, None
    return pos, Token.Whitespace, str[:pos]

def isOperator(str):
    if DebugRecognizerNames:
        print("isOperator")
    opers = [op for op in Operators if str.startswith(op)]
    opers.sort(key=lambda a: -len(a))
    if len(opers):
        return len(opers[0]), Tokens[opers[0]], str[:len(opers[0])]
    else:
        return 0, None, None

def isPunctuator(str):
    if DebugRecognizerNames:
        print("isPunctuator")
    if str[0] in Punctuators:
        return 1, Tokens[str[0]], str[:1]
    else:
        return 0, None, None

def isKeyword(str):
    if DebugRecognizerNames:
        print("isKeyword")
    for keyword in Keywords:
        if str.startswith(keyword):
            return len(keyword), Tokens[keyword], str[:len(keyword)]
    return 0, None, None

def isIdentifier(str):
    if DebugRecognizerNames:
        print("isIdentifier")
    if str[0] == '@':
        size, token, str = isKeyword(str[1:])
        if size != 0:
            return size+1, Token.Identifier, str[:size+1]
    if str[0].isalpha() or str[0]=='_':
        pos = 0
        while pos < len(str) and (str[pos].isalpha() or str[pos].isdigit() or str[pos]=='_'):
            pos+=1
        return pos, Token.Identifier, str[:pos]
    return 0, None, None

class NumericLiteralFSM(FiniteStateMachine):

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
        self.add_state('s7', self.s7_handler, True)
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
        else:
            return 's7', str
        if str[self.pos] == '.':
            self.pos+=1
            return 's2', str
        if str[self.pos] == 'E' or str[self.pos] == 'e':
            self.pos+=1
            return 's4', str
        return 'exit_state', str

    def s2_handler(self, str):
        if str[self.pos].isdigit():
            self.pos+=1
            return 's3', str
        return 'exit_state', str

    def s3_handler(self, str):
        if str[self.pos].isdigit():
            self.pos+=1
            return 's3', str
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
        return 's7', str

    def s7_handler(self, str):
        return None, str

    def exit_handler(self, str):
        return None, str

def isNumericLiteral(str):
    if DebugRecognizerNames:
        print("isNumericLiteral")
    numericLiteralFSM = NumericLiteralFSM()
    state, pos = numericLiteralFSM.run(str)
    if state == 's7':
        return pos, NumericLiteral, str[:pos]
    else:
        return 0, None, None

def isCharacterLiteral(str):
    if DebugRecognizerNames:
        print("isCharacterLiteral")
    if (len(str) >= 7 and str[0]=='\''
       and ( str[1]=='u' or str[1]=='x' )
       and (str[2].isdigit() and str[3].isidigit() and str[4].isdigit() and str[5].isdigit())
       and str[6] == '\''):
        return 7, CharacterLiteral, str[:7]
    if len(str) >= 4 and str[0]=='\'' and str[1]=='\\' and str[3]=='\'':
        return 4, CharacterLiteral, str[:4]
    if len(str) >= 3 and str[0]=='\'' and str[2]=='\'':
        return 3, CharacterLiteral, str[:3]
    return 0, None, None

def isStringLiteral(str):
    if DebugRecognizerNames:
        print("isStringLiteral")
    # todo: String Interpolation
    if len(str) >= 2:
        pos = 0
        Verbatim = False
        Interpolation = False
        if str[pos]=='@':
            pos+=1
            Verbatim = True
        if str[pos]=='$':
            pos+=1
            Interpolation=True
        if str[pos] == '"':
            while pos < len(str):
                if pos + 1 < len(str):
                    if ((Verbatim and not str[pos]=='"' and str[pos+1] == '"') or
                        (not Verbatim and not str[pos]=='\\' and str[pos+1]=='"')):
                        return pos+2, StringLiteral, str[:pos+2]
                pos += 1
    return 0, None, None


class CSharpLexer:

    recognizers = [ isWhiteSpace,
                    isComment,
                    isMultilineComment,
                    isKeyword,
                    isIdentifier,
                    isPunctuator,
                    isOperator,
                    isStringLiteral,
                    isCharacterLiteral,
                    isNumericLiteral ] # todo: bool literal null literal

    def __init__(self, str):
        self.str = str
        self.pos=0
        # fsm.add_state()

    def nextToken(self):
        if self.pos >= len(self.str):
            return Token.EndOfInput, ""
        for recognizer in self.recognizers:
            delta_pos, token_type, value = recognizer(self.str[self.pos:])
            if delta_pos != 0:
                self.pos += delta_pos
                return token_type, value
        return Token.Error, ""

lexer = CSharpLexer("""
using System;

namespace HelloWorld
{
  class Program
  {
    static void Main(string[] args)
    {
      Console.WriteLine("Hello World!");
    }
  }
}
""")
lexer.nextToken()
