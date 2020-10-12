from CSharpLangDefs import *

class ASTNode:
    Val = None
    Children = []

    def __init__(self, Val):
        self.Val = Val

    def add_child(self, Child):
        if not isinstance(Child, ASTNode):
            return False
        self.Children.append(Child)
        return True

    def get_child(self, ind):
        return self.Children[ind]

    def __str__(self):
        return '{' + self.Val.__repr__() + '}'

# aux functions

def remove_whitespaces(stack):
    return [(i, stack[i]) for i in range(len(stack)) if stack[i].Val not in [Tokens['whitespace'], Comment, CommentMultiline] ]

def get_val(s, pos):
    if pos >= len(s):
        return None
    return s[pos][1].Val

# def copy_tree(root):
#     if not root:
#         return None
#     return ASTNode(root.Val, copy_tree(Left), copy_tree(Right))

class SyntaxRule:
    From = []
    To = None

    def __init__(self, From, To):
        self.From = From
        self.To = To

    def check(self, stack):
        if len(stack) < len(self.From):
            return 0
        for i in range(len(self.From)):
            if get_val(stack, i) not in self.From[i]:
                return 0
        return stack[len(self.From)-1][0]+1

    def reduce(self, stack):
        matched_tokens_num = self.check(remove_whitespaces(stack))
        if matched_tokens_num == 0:
            return stack, False

        TreeValues = stack[:matched_tokens_num]
        NewTree = ASTNode(self.To)
        for tv in TreeValues:
            NewTree.add_child(tv)
        stack = stack[matched_tokens_num:]
        stack.insert(0, NewTree)
        return stack, True

class ClassDeclRule(SyntaxRule):
    def __init__(self):
        self.To = NonTerm.ClassDecl

    def check(self, s):
        pos = 0
        if get_val(s, pos) == NonTerm.Block:
            pos+=1
            if get_val(s, pos) == Identifier and s[pos+1][1].Val == Tokens[':']: # todo: support multiple inheritancew
                pos+=2
            if get_val(s, pos) == Identifier and s[pos+1][1].Val == Tokens['class']:
                pos+=2
                while get_val(s, pos) in class_modifiers:
                    pos+=1
                return s[pos-1][0]+1
        return 0

class FuncDeclRule(SyntaxRule):
    def __init__(self):
        self.To = NonTerm.FuncDecl

    def check(self, s):
        pos = 0
        if get_val(s, pos) == NonTerm.Block:
            pos+=1

            if get_val(s, pos) == Tokens[')']:
                pos+=1
                while get_val(s, pos) == Identifier and get_val(s, pos+1) in [Identifier]+[Tokens[i] for i in Types] and get_val(s, pos+2) == Tokens[',']:
                    pos+3
                if get_val(s, pos) == Identifier and get_val(s, pos+1) in [Identifier]+[Tokens[i] for i in Types]:
                    pos+=2
                    if get_val(s, pos) == Tokens['('] and get_val(s, pos+1) == Identifier and get_val(s, pos+2) in [Identifier]+[Tokens[i] for i in Types]:
                        pos+=3

                        if get_val(s, pos) == Tokens['delegate']:
                            pos+=1

                        if get_val(s, pos) == Tokens['static']:
                            pos+=1

                        if get_val(s, pos) in access_modifiers:
                            pos+=1
                        if get_val(s, pos) in access_modifiers:
                            pos+=1

                        return s[pos-1][0]+1
        return 0

class BlockRule(SyntaxRule):
    def __init__(self):
        self.To = NonTerm.Block

    # line, if, while, switch, {}, for
    def check(self, s):
        pos=0
        if get_val(s, pos) == Tokens['}']:
            pos+=1
            while get_val(s, pos) == NonTerm.Line:
                pos+=1
        if get_val(s, pos) == Tokens['{']:
            return s[pos][0]+1
        return 0

class IfRule(SyntaxRule):
    def __init__(self):
        self.To = NonTerm.IfBlock

    def check(self, s):
        pos=0
        if get_val(s, pos) == NonTerm.Block or get_val(s, pos) == NonTerm.Line:
            pos+=1
            if (get_val(s, pos) == NonTerm.Condition or get_val(s, pos) == NonTerm.Expression) and get_val(s, pos+1) == Tokens['if']: # todo: not match unbracketed expresions
                return s[pos+1][0]+1
        return 0

class IfElseRule(SyntaxRule):
    def __init__(self):
        self.To = NonTerm.IfElseBlock

    def check(self, s):
        pos=0
        if get_val(s, pos) == NonTerm.Block or get_val(s, pos) == NonTerm.Line:
            pos+=1
            if get_val(s, pos) == Tokens['else']:
                pos+=1
                if get_val(s, pos) == NonTerm.IfBlock:
                    return s[pos][0]+1
        return 0

class SwitchRule(SyntaxRule):
    def __init__(self):
        self.To = NonTerm.SwitchBlock

    def check(self, s):
        pos=0
        if get_val(s, pos) == NonTerm.SwitchBody and get_val(s, pos+1) == Tokens['switch']:
            return s[pos+1][0]+1
        return 0

class SwitchBodyRule(SyntaxRule):
    def __init__(self):
        self.To = NonTerm.SwitchBody

    def check(self, s):
        pos=0
        if get_val(s, pos) == '}':
            pos+=1
            while get_val(s, pos) == NonTerm.CaseBlock:
                pos+=1
            if get_val(s, pos) == '{':
                return s[pos][0]+1
        return 0

#template
class CaseRule(SyntaxRule):
    def __init__(self):
        self.To = NonTerm.CaseBlock

    def check(self, s):
        pos=0
        if get_val(s, pos) == Tokens[';'] and get_val(s, pos+1) == Tokens['break']:
            pos+=2
            while get_val(s, pos) == NonTerm.Line or get_val(s, pos) == NonTerm.Block:
                pos+=1
            if get_val(s, pos) == Tokens[':'] and get_val(s, pos+1) == Literal and get_val(s, pos+2) == Tokens['case']:
                return s[pos+2][0]+1
        return 0


class IdentifierRule(SyntaxRule):
    def __init__(self):
        self.To = NonTerm.ComplexIdentifier

    def check(self, s):
        pos = 0
        if not (get_val(s, pos) == Identifier and get_val(s, pos+1) == Tokens['.']):
            return 0
        while get_val(s, pos) == Identifier and get_val(s, pos+1) == Tokens['.']:
            pos+=2
        if get_val(s, pos) == Identifier:
            return s[pos][0]+1
        else:
            return 0


#template
class AssignmentRule(SyntaxRule):
    def __init__(self):
        self.To = NonTerm.Assignment

    def check(self, s):
        pos=0
        if get_val(s, pos) in [Literal, Identifier, NonTerm.ComplexIdentifier, NonTerm.Condition, NonTerm.Expression, NonTerm.TernaryOperator, NonTerm.Assignment, NonTerm.CallFuncOrMethod]:
            pos+=1
            if get_val(s, pos)== Tokens['new']:
                pos+=1
            if get_val(s, pos) == Tokens['='] and get_val(s, pos+1) in[Identifier, NonTerm.ComplexIdentifier]:
                pos+=2
                if get_val(s, pos) == Identifier:
                    pos+=1
                return s[pos-1][0]+1
        return 0

class ArrayRule(SyntaxRule):
    def __init__(self):
        pass

    def check(self, s):
        pos = 0
        if get_val(s, pos) == Tokens[']']:
            pos+=1
            if get_val(s, pos) == NumericLiteral:
                pos+=1
            if get_val(s, pos) == Tokens['[']:
                if get_val(s, pos+1) in [Identifier]+[Tokens[i] for i in Types]:
                    self.To = Identifier
                    return s[pos+1][0]+1
                elif get_val(s, pos+1) == NonTerm.ComplexIdentifier:
                    self.To = NonTerm.ComplexIdentifier
                    return s[pos+1][0]+1
        return 0


class CallFuncOrMethodRule(SyntaxRule):
    def __init__(self):
        self.To = NonTerm.CallFuncOrMethod

    def check(self, s):
        pos=0
        if get_val(s, pos)==Tokens[')']:
            pos+=1
            while get_val(s, pos) in [Literal, Identifier, NonTerm.ComplexIdentifier, NonTerm.Condition, NonTerm.Expression, NonTerm.TernaryOperator, NonTerm.Assignment, NonTerm.CallFuncOrMethod]:
                pos+=1
                if get_val(s, pos) != Tokens[',']:
                    break
                else:
                    pos+=1
            if get_val(s, pos)==Tokens['('] and get_val(s, pos+1) in [Identifier, NonTerm.ComplexIdentifier]:
                return s[pos+1][0]+1
        #todo: potertial trouble with ()
#        if get_val(s, pos) == NonTerm.Expression:

        return 0



#template
class ForLoopRule(SyntaxRule):
    def __init__(self):
        self.To = NonTerm.ForLoop

    def check(self, s):
        pos=0
        if get_val(s, pos)==NonTerm.Block or get_val(s, pos) == NonTerm.Line:
            pos+=1
            if get_val(s, pos)==Tokens[')']:
                if get_val(s, pos+1) == Tokens[';']:
                    pos+=1
                elif get_val(s, pos+2)==Tokens[';']:
                    pos+=2
                else:
                    return 0
                if get_val(s, pos+1) == Tokens[';']:
                    pos+=1
                elif get_val(s, pos+2)==Tokens[';']:
                    pos+=2
                else:
                    return 0
                if get_val(s, pos)==Tokens['('] and get_val(s, pos+1)==Tokens['for']:
                    return s[pos+1][0]+1
        return 0

#template
class WhileRule(SyntaxRule):
    def __init__(self):
        self.To = NonTerm.WhileLoop

    def check(self, s):
        pos=0
        if get_val(s, pos) == NonTerm.Block or get_val(s, pos) == NonTerm.Line:
            pos+=1
            if (get_val(s, pos) == NonTerm.Condition or get_val(s, pos) == NonTerm.Expression) and get_val(s, pos+1) == Tokens['while']: # todo: not match unbracketed expresions
                return s[pos+1][0]+1
        return 0

#template
class LineRule(SyntaxRule):
    def __init__(self):
        self.To = NonTerm.Line

    def check(self, s):
        pos=0
        if get_val(s, pos) == Tokens[';'] and get_val(s, pos+1) in [NonTerm.Assignment, NonTerm.CallFuncOrMethod, NonTerm.Await]:
            return 0
        return 0

#template
class SimpleLineRule(SyntaxRule):
    def __init__(self):
        self.To = NonTerm.Line

    def check(self, s):
        pos=0
        if get_val(s, pos) == Tokens[';']:
            pos+=1
            while get_val(s, pos) not in [Tokens[';'], Tokens['{'], Tokens['}']]:
                pos+=1
            return s[pos-1][0]+1
        return 0

class SimpleBlockRule(SyntaxRule):
    def __init__(self):
        self.To = NonTerm.Block

    def check(self, s):
        pos=0
        if get_val(s, pos) == Tokens['}']:
            pos+=1
            while get_val(s, pos) in [NonTerm.Line, NonTerm.ClassDecl, NonTerm.FuncDecl]:
                pos+=1
            if get_val(s, pos) == Tokens['{']:
                return s[pos][0]+1
        return 0

class BlockWrapRule(SyntaxRule):
    def __init__(self):
        self.To = NonTerm.BlockWrap

    def check(self,s):
        pos=0
        if get_val(s, pos) == NonTerm.Block:
            pos+=1
            if get_val(s, pos) not in[None, Tokens[';'], Tokens['}']]:
                while get_val(s, pos) not in[None, Tokens[';'], Tokens['}']]:
                    pos+=1
                return s[pos-1][0]+1
            # if get_val(s, pos)==Tokens[')']:
            #     while get_val(s, pos) != Tokens['(']:
            #         pos+=1
            # if get_val(s, pos) == Identifier:
            #     pos+=1
            #     if get_val(s, pos) == Identifier:
            #         pos+=1
            #
        return 0

#template
class Rule(SyntaxRule):
    def __init__(self):
        self.To = NonTerm.Token

    def check(self, s):
        pos=0
        return 0
