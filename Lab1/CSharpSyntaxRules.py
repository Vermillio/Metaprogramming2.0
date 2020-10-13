from CSharpLangDefs import *
import itertools

def block_width(block):
    try:
        return block.index('\n')
    except ValueError:
        return len(block)

def stack_str_blocks(blocks):
    """Takes a list of multiline strings, and stacks them horizontally.

    For example, given 'aaa\naaa' and 'bbbb\nbbbb', it returns
    'aaa bbbb\naaa bbbb'.  As in:

    'aaa  +  'bbbb   =  'aaa bbbb
     aaa'     bbbb'      aaa bbbb'

    Each block must be rectangular (all lines are the same length), but blocks
    can be different sizes.
    """
    builder = []
    block_lens = [block_width(bl) for bl in blocks]
    split_blocks = [bl.split('\n') for bl in blocks]

    for line_list in itertools.zip_longest(*split_blocks, fillvalue=None):
        for i, line in enumerate(line_list):
            if line is None:
                builder.append(' ' * block_lens[i])
            else:
                builder.append(line)
            if i != len(line_list) - 1:
                builder.append(' ')  # Padding
        builder.append('\n')

    return ''.join(builder[:-1])

class ASTNode:
    Val = None
    Pos = None

    def __init__(self, Val, Pos, WsTemplate):
        self.Val = Val
        self.Pos = Pos
        self.WsTemplate = WsTemplate
        self.Children = []

    def add_child(self, Child):
        if not isinstance(Child, ASTNode):
            return False
        self.Children.append(Child)
        return True

    def get_child(self, ind):
        return self.Children[ind]

    def __str__(self):
        return '{' + self.Val.__repr__() + '}'

    def replace_whitespaces(self, symbols):
        return [symbols[ws] for ws in WsTemplate]

    def display(self): # Here
        if not self.Children:
            return self.__str__()

        child_strs = [child.display() for child in self.Children]
        child_widths = [block_width(s) for s in child_strs]

        # How wide is this block?
        display_width = max(len(self.__str__()),
                    sum(child_widths) + len(child_widths) - 1)

        # Determines midpoints of child blocks
        child_midpoints = []
        child_end = 0
        for width in child_widths:
            child_midpoints.append(child_end + (width // 2))
            child_end += width + 1

        # Builds up the brace, using the child midpoints
        brace_builder = []
        for i in range(display_width):
            if i < child_midpoints[0] or i > child_midpoints[-1]:
                brace_builder.append(' ')
            elif i in child_midpoints:
                brace_builder.append('+')
            else:
                brace_builder.append('-')
        brace = ''.join(brace_builder)

        name_str = '{:^{}}'.format(self.__str__(), display_width)
        below = stack_str_blocks(child_strs)

        return name_str + '\n' + brace + '\n' + below

# aux functions
#
# def remove_whitespaces(stack):
#     return [(i, stack[i]) for i in range(len(stack)) if stack[i].Val not in [Tokens['whitespace'], Comment, CommentMultiline] ]

def get_val(s, pos):
    if pos >= len(s):
        return None
    return s[pos].Val

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
        return len(self.From)

    def reduce(self, stack):
        matched_tokens_num = self.check(stack)
        if matched_tokens_num == 0:
            return stack, False

        TreeValues = stack[:matched_tokens_num]
        NewTree = ASTNode(self.To, None, None)
        for tv in TreeValues:
            NewTree.add_child(tv)
        print('!'+str(len(TreeValues)))
        print(NewTree.Val)
        stack = stack[matched_tokens_num:]
        stack.insert(0, NewTree)
        return stack, True

class ClassDeclRule(SyntaxRule):
    def __init__(self):
        self.To = NonTerm.ClassDecl

    def check(self, s):
        pos = 0
        ws_template = []
        if get_val(s, pos) == NonTerm.Block:
            pos+=1
            if get_val(s, pos) == Identifier and get_val(s, pos+1) == Tokens[':']: # todo: support multiple inheritancew
                pos+=2
            if get_val(s, pos) == Identifier and get_val(s, pos+1) == Tokens['class']:
                pos+=2
                while get_val(s, pos) in class_modifiers:
                    pos+=1
                return pos
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
                        return pos
        return 0

class IfRule(SyntaxRule):
    def __init__(self):
        self.To = NonTerm.IfBlock

    def check(self, s):
        pos=0
        if get_val(s, pos) == NonTerm.Block or get_val(s, pos) == NonTerm.Line:
            pos+=1
            if (get_val(s, pos) == NonTerm.Condition or get_val(s, pos) == NonTerm.Expression) and get_val(s, pos+1) == Tokens['if']: # todo: not match unbracketed expresions
                return pos+2
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
                    return pos+1
        return 0

class SwitchRule(SyntaxRule):
    def __init__(self):
        self.To = NonTerm.SwitchBlock

    def check(self, s):
        pos=0
        if get_val(s, pos) == NonTerm.SwitchBody and get_val(s, pos+1)==Tokens[')'] and get_val(s, pos+2) == Identifier and get_val(s, pos+3)==Tokens['('] and get_val(s, pos+4) == Tokens['switch']:
            return pos+5
        return 0

class SwitchBodyRule(SyntaxRule):
    def __init__(self):
        self.To = NonTerm.SwitchBody

    def check(self, s):
        pos=0
        if get_val(s, pos) == Tokens['}']:
            pos+=1
            if get_val(s, pos) != NonTerm.CaseBlock:
                return 0
            while get_val(s, pos) == NonTerm.CaseBlock:
                pos+=1
            if get_val(s, pos) == Tokens['{']:
                return pos+1
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
            if get_val(s, pos) == Tokens[':']:
                if get_val(s, pos+1) == Tokens['default']:
                    return pos+2
                if get_val(s, pos+1) in Literals and get_val(s, pos+2) == Tokens['case']:
                    return pos+3
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
            return pos+1
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
                return pos
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
                    return pos+2
                elif get_val(s, pos+1) == NonTerm.ComplexIdentifier:
                    self.To = NonTerm.ComplexIdentifier
                    return pos+2
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
                return pos+2
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
                pos+=1
                if get_val(s, pos) == Tokens[';']:
                    pos+=1
                elif get_val(s, pos+1)==Tokens[';']:
                    pos+=2
                else:
                    return 0
                if get_val(s, pos) == Tokens[';']:
                    pos+=1
                elif get_val(s, pos+1)==Tokens[';']:
                    pos+=2
                else:
                    return 0

                if get_val(s, pos)==Tokens['('] and get_val(s, pos+1)==Tokens['for']:
                    return pos+2
        return 0

#template
class WhileRule(SyntaxRule):
    def __init__(self):
        self.To = NonTerm.WhileLoop

    def check(self, s):
        pos=0
        if get_val(s, pos) == NonTerm.Block or get_val(s, pos) == NonTerm.Line:
            pos+=1
            if get_val(s, pos) == Tokens[')'] and (get_val(s, pos+1) == NonTerm.Condition or get_val(s, pos+1) == NonTerm.Expression or get_val(s, pos+1) == Identifier) and get_val(s, pos+2) == Tokens['('] and get_val(s, pos+3) == Tokens['while']:
                return pos+4
        pos=0
        if get_val(s, pos) == Tokens[')'] and (get_val(s, pos+1) == NonTerm.Condition or get_val(s, pos+1) == NonTerm.Expression or get_val(s, pos+1) == Identifier) and get_val(s, pos+2) == Tokens['('] and get_val(s, pos+3) == Tokens['while']:
            pos+=4
            if get_val(s, pos) == NonTerm.Block or get_val(s, pos) == NonTerm.Line:
                pos+=1
                if get_val(s, pos) == Tokens['do']:
                    return pos+1
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
            while pos < len(s) and get_val(s, pos) not in [Tokens[';'], Tokens['{'], Tokens['}']]:
                if get_val(s, pos) in [Tokens['('], Tokens[')']]:
                    return 0
                pos+=1
            return pos
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
                return pos+1
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
                return pos
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
