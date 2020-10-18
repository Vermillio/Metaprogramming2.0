from CSharpLangDefs import *
import itertools
from config import *


def apply_indent(str, indent):
    indent_str = indent_size * indent * ('\t' if indent_style == 'tab' else ' ')
    return str + indent_str if str == '\n' else str

class Code:
    tokens=[]
    whitespaces=[]
    indents=[]

    def __init__(self, tokens, whitespaces):
        self.tokens = tokens
        self.whitespaces = whitespaces
        self.indents=[0]*len(tokens)

    def get_token(self, i):
        if i >= len(self.tokens):
            return None
        return self.tokens[i][0]

    def index(self, token, start, end):
        i = start
        while i < end:
            current = self.get_token(i)
            if current == token:
                return i
        return -1

    def set_space_after(self, i, ws):
        if ws != None:
            self.whitespaces[i+1] = ws

    def set_space_before(self, i, ws):
        if ws != None:
            self.whitespaces[i] = ws

    def get_space_before(self, i):
        return self.whitespaces[i]

    def get_space_after(self, i):
        return self.whitespaces[i+1]

    def set_indent(self, i, indent):
        self.indents[i] = indent

    def inc_indent(self, i):
        self.indents[i]+=1

    def dec_indent(self, i):
        self.indents[i]-=1

    def get_str(self):
        str = [apply_indent(self.tokens[i][1], self.indents[i]) for i in range(len(self.tokens))]
#        str.insert(0, self.add_indent(whitespaces[0]), indents[0])
        for i in range(0, len(self.indents)):
            str.insert(2*i, apply_indent(self.whitespaces[i], self.indents[i]))
        if insert_final_newline:
            str+=['\n']
        return ''.join(str)


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

    def __init__(self, Val, Start, End):
        self.Val = Val
        self.Start = Start
        self.End = End
        self.Children = []
        self.indent = 0

    def add_child(self, Child):
        if not isinstance(Child, ASTNode):
            return False
        self.Children.append(Child)
        return True

    def get_child(self, ind):
        return self.Children[ind]

    def __str__(self):
        return '{' + self.Val.__repr__() + '}'

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

def get_val(s, pos):
    if pos >= len(s):
        return None
    return s[pos].Val

class SyntaxRule:
    NodeToken = None
    code = None

    def apply_ws(self, start, end):
        pass

    def __init__(self, From, NodeToken):
        self.NodeToken = NodeToken

    def check(self, stack):
        return 0

    def reduce(self, stack):
        matched_tokens_num = self.check(stack)
        if matched_tokens_num == 0:
            return stack, False

        TreeValues = stack[:matched_tokens_num]
        TreeValues.reverse()

        if self.NodeToken != None:
            NewTree = ASTNode(self.NodeToken, TreeValues[0].Start, TreeValues[-1].End)
            for i in range(len(TreeValues)):
                tv = TreeValues[i]
                NewTree.add_child(tv)
            stack = stack[matched_tokens_num:]
            stack.insert(0, NewTree)

        self.apply_ws(TreeValues[0].Start, TreeValues[-1].End)
        return stack, True

class ClassDeclRule(SyntaxRule):
    def __init__(self):
        self.NodeToken = NonTerm.ClassDecl

    def apply_ws(self, start, end):
        for pos in range(start, end):
            token = self.code.get_token(pos)
            if token == Tokens[':']:
                self.code.set_space_after(pos, ' ' if csharp_space_after_colon_in_inheritance_clause else '')
                self.code.set_space_before(pos, ' ' if csharp_space_before_colon_in_inheritance_clause else '')
            else:
                self.code.set_space_after(pos, ' ')

    def check(self, s):
        pos = 0
        if get_val(s, pos) in [Identifier, NonTerm.ComplexIdentifier] and get_val(s, pos+1) == Tokens[':']: # todo: support multiple inheritancew
            pos+=2
        if get_val(s, pos) == NonTerm.Generic:
            pos+=1
        if get_val(s, pos) == Identifier and (get_val(s, pos+1) == Tokens['class'] or get_val(s, pos+1) == Tokens['struct'] or get_val(s, pos+1) == Tokens['interface']):
            pos+=2
            while get_val(s, pos) in class_modifiers:
                pos+=1
            return pos
        return 0

class MethodDeclRule(SyntaxRule):
    def __init__(self):
        self.NodeToken = NonTerm.MethodDecl

    def apply_ws(self, start, end):
        for pos in range(start, end):
            token = self.code.get_token(pos)
            if token == Tokens['(']:
                self.code.set_space_before(pos, ' ' if csharp_space_between_method_declaration_name_and_open_parenthesis else '')
                if self.code.get_token(pos+1) == Tokens[')']:
                    self.code.set_space_after(pos, ' ' if csharp_space_between_method_declaration_empty_parameter_list_parentheses else '')
                else:
                    self.code.set_space_after(pos, ' ' if csharp_space_between_method_declaration_parameter_list_parentheses else '')
            elif token == Tokens[')']:
                if self.code.get_token(pos-1)==Tokens['(']:
                    self.code.set_space_before(pos, ' ' if csharp_space_between_method_declaration_empty_parameter_list_parentheses else '')
                    pass
                else:
                    self.code.set_space_before(pos, ' ' if csharp_space_between_method_declaration_parameter_list_parentheses else '')

    def check(self, s):
        pos = 0
        if get_val(s, pos) == NonTerm.Parentheses:
            pos+=1
            if get_val(s, pos) == NonTerm.Generic:
                pos+=1
            if get_val(s, pos) == Identifier:
                pos+=1
                if get_val(s, pos) in [Identifier]+[Tokens[i] for i in Types]:
                    pos+=1
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

# class NamespaceRule(SyntaxRule):
#     def __init__(self):
#         self.NodeToken = NonTerm.NamespaceBlock
#
#     def check(self, s):
#         pos = 0
#         if get_val(s, pos) == NonTerm.Block and get_val(s, pos+1) in [Identifier, NonTerm.ComplexIdentifier] and get_val(s, pos+2) == Tokens['namespace']:
#             return pos+3
#         return 0

class GenericRule(SyntaxRule):
    def __init__(self):
        self.NodeToken = NonTerm.Generic

    def apply_ws(self, start, end):
        self.code.set_space_after(start, '')
        self.code.set_space_before(end-1, '')

    def check(self, s):
        pos=0
        if get_val(s, pos) == Tokens['>'] and get_val(s, pos+1) in [Identifier] and get_val(s, pos+2) == Tokens['<']:
            return pos+3
        return 0

class SwitchIndentRule(SyntaxRule):
    def __init__(self):
         self.NodeToken = NonTerm.SwitchBlock

    def apply_ws(self, start, end):
        index_of_block = self.code.index(Tokens['{'], start, end)
        pos = index_of_block+1
        while pos < end-1:
            token = self.code.get_token(pos)
            if csharp_indent_switch_labels:
                self.code.inc_indent(pos)
            if csharp_indent_case_contents and token != Tokens['case']:
                self.code.inc_indent(pos)
            if token == Tokens['case']:
                self.code.set_space_before(pos, '\n')


    def check(self, s):
        pos=0
        if get_val(s, 0) == NonTerm.Block and get_val(s, 1) == NonTerm.Switch:
            return 2
        return 0

class IdentifierRule(SyntaxRule):
    def __init__(self):
        self.NodeToken = NonTerm.ComplexIdentifier

    def apply_ws(self, start, end):
        for pos in range(start, end-1):
            self.code.set_space_after(pos, '')

    def check(self, s):
        pos = 0
        if not (get_val(s, pos) == Identifier or get_val(s, pos) == NonTerm.ComplexIdentifier) and get_val(s, pos+1) == Tokens['.']:
            return 0
        while (get_val(s, pos) == Identifier or get_val(s, pos) == NonTerm.ComplexIdentifier) and get_val(s, pos+1) == Tokens['.']:
            pos += 2
        if pos != 0 and (get_val(s, pos) == Identifier or get_val(s, pos) == NonTerm.ComplexIdentifier):
            return pos+1
        return 0

#class DeclarationRule(SyntaxRule)
#
#
# #template
# class AssignmentRule(SyntaxRule):
#     def __init__(self):
#         self.NodeToken = NonTerm.Assignment
#
#     def check(self, s):
#         pos=0
#         if get_val(s, pos) in [Literal, Identifier, NonTerm.ComplexIdentifier, NonTerm.Condition, NonTerm.Expression, NonTerm.TernaryOperator, NonTerm.Assignment, NonTerm.CallFuncOrMethod]:
#             pos+=1
#             if get_val(s, pos)== Tokens['new']:
#                 pos+=1
#             if get_val(s, pos) == Tokens['='] and get_val(s, pos+1) in[Identifier, NonTerm.ComplexIdentifier]:
#                 pos+=2
#                 if get_val(s, pos) == Identifier:
#                     pos+=1
#                 return pos
#         return 0

class MethodCallRule(SyntaxRule):
    def __init__(self):
        self.NodeToken = NonTerm.MethodCall

    def apply_ws(self, start, end):
        for pos in range(start, end):
            token = self.code.get_token(pos)
            if token == Tokens['(']:
                self.code.set_space_before(pos, ' ' if csharp_space_between_method_call_name_and_opening_parenthesis else '')
                self.code.set_space_after(pos, ' ' if csharp_space_between_method_call_parameter_list_parentheses else '')
            elif token == Tokens[')']:
                self.code.set_space_before(pos, ' ' if csharp_space_between_method_call_parameter_list_parentheses else '')

    def check(self, s):
        pos=0
        if get_val(s, pos) == NonTerm.Parentheses:
            pos+=1
            if get_val(s, pos) in [Identifier, NonTerm.ComplexIdentifier]:
                return pos+1
        return 0

# #template
# class SimpleLineRule(SyntaxRule):
#     def __init__(self):
#         self.NodeToken = NonTerm.Line
#
#     def check(self, s):
#         pos=0
#         ws = [None]
#         if get_val(s, pos) == Tokens[';']:
#             pos+=1
#             ws+=[None]
#             while pos < len(s) and get_val(s, pos) not in [Tokens[';'], Tokens['{'], Tokens['}'], NonTerm.Line]:
#                 if get_val(s, pos) in [Tokens['('], Tokens[')']]:
#                     return 0, None
#                 pos+=1
#                 ws+= [None]
#             return pos, ws
#         return 0, None

class SimpleBlockRule(SyntaxRule):
    def __init__(self):
        self.NodeToken = NonTerm.Block

    def apply_ws(self, start, end):
        is_single_line_block = True
        for pos in range(start, end-1):
            space = self.code.get_space_after(pos)
            if '\n' in space:
                is_single_line_block = False

        for pos in range(start+1, end-1):
            token = self.code.get_token(pos)
            if token == NonTerm.EmptyLine:
                is_single_line_block = False
            pos+=1

        if is_single_line_block and csharp_preserve_single_line_blocks:
            self.code.set_space_after(start, '')
            self.code.set_space_before(end-1, '')
        else:
            self.code.set_space_after(start, '\n')
            self.code.set_space_before(end-1, '\n')
        self.code.set_space_after(end-1, '\n')

        # indent
        if csharp_indent_block_contents:
            pos = start+1
            for pos in range(start+1, end-1):
                self.code.inc_indent(pos)

        if csharp_indent_braces:
            self.code.inc_indent(start)
            self.code.inc_indent(end-1)

    def check(self, s):
        pos=0
        if get_val(s, pos) == Tokens['}']:
            pos+=1
            while pos < len(s) and get_val(s, pos) != Tokens['{']:
                pos+=1
            if get_val(s, pos) == Tokens['{']:
                return pos+1
        return 0

#template
class UsingRule(SyntaxRule):
    def __init__(self):
        self.NodeToken = NonTerm.Using

    def check(self, s):
        if get_val(s, 0) in [Identifier, NonTerm.ComplexIdentifier] and get_val(s, 1) == Tokens['using']:
            return 2
        return 0

# #template
# class LineRule(SyntaxRule):
#     def __init__(self):
#         self.NodeToken = NonTerm.TopLevel
#
#     def check(self, s):
#         pos=0
#         #ws = [None]
#         if get_val(s, pos) == Tokens['\n']:
#             pos+=1
#             ws+=[None]
#             while pos < len(s) and get_val(s, pos) not in [Tokens['{'], Tokens['}'], NonTerm.Line]:
#                 if get_val(s, pos) in [Tokens['('], Tokens[')']]:
#                     return 0, None
#                 pos+=1
#                 ws+= [None]
#             return pos, ws
#         return 0, None
#         return len(s), [None]*(len(s)+1)

#template
class ControlFlowRule(SyntaxRule):
    def __init__(self):
        pass

    def apply_ws(self, start, end):
        self.code.set_space_after(start, ' ' if csharp_space_after_keywords_in_control_flow_statements else '')
        keyword = self.code.get_token(start)
        if keyword == Tokens['for']:
            for pos in range(start+1, end):
                token = self.code.get_token(pos)
                if token == Tokens[';']:
                    token.set_space_before(' ' if csharp_space_before_semicolon_in_for_statement else '')
                    token.set_space_after(' ' if csharp_space_after_semicolon_in_for_statement else '')

    def check(self, s):
        pos=0
        if get_val(s, pos) == NonTerm.Parentheses:
            pos+=1
            if get_val(s, pos) in [Tokens['if'], Tokens['while'], Tokens['for'], Tokens['foreach'], Tokens['switch']]:
                if get_val(s, pos) == Tokens['switch']:
                    self.NodeToken = NonTerm.Switch
                else:
                    self.NodeToken = NonTerm.ControlFlow
                return pos+1
        return 0

class ParenthesesRule(SyntaxRule):
    def __init__(self):
        self.NodeToken = NonTerm.Parentheses

    def apply_ws(self, start, end):
        self.code.set_space_after(start, ' ' if csharp_space_between_parentheses else '')
        self.code.set_space_before(end-1, ' ' if csharp_space_between_parentheses else '')

    def check(self, s):
        pos=0
        if get_val(s, pos) == Tokens[')']:
            while pos < len(s) and get_val(s, pos) != Tokens['(']:
                pos+=1
            if get_val(s, pos) == Tokens['(']:
                return pos+1
        return 0

class SquareBracketsRule(SyntaxRule):
    def __init__(self):
        self.NodeToken = NonTerm.SquareBrackets

    def apply_ws(self, start, end):
        self.code.set_space_before(start, ' ' if csharp_space_before_open_square_brackets else '')
        if end == start+2:
            self.code.set_space_after(start, ' ' if csharp_space_between_empty_square_brackets else '')
        else:
            self.code.set_space_after(start, ' ' if csharp_space_between_square_brackets else '')
            self.code.set_space_before(end-1, ' ' if csharp_space_between_square_brackets else '')

    def check(self, s):
        pos = 0
        if get_val(s, pos) == Tokens[']']:
            pos+=1
            while get_val(s, pos) != Tokens['[']:
                pos+=1
            if get_val(s, pos) == Tokens['[']:
                return pos+1
        return 0

class ObjectInitializerRule(SyntaxRule):
    def __init__(self):
        self.NodeToken = NonTerm.ObjectInitializer

    def apply_ws(self, start, end):
        pos = start
        while pos < end:
            token = self.code.get_token(pos)
            if token == Tokens[',']:
                self.code.set_space_after(pos, '\n' if csharp_new_line_before_members_in_object_initializers else ' ')
            pos+=1

    def check(self, s):
        pos = 0
        if get_val(s, pos) == NonTerm.Block:
            pos+=1
            if get_val(s, pos) == NonTerm.Parentheses:
                pos+=1
            if get_val(s, pos) == Identifier:
                return pos
        return 0

class AnonymousTypeRule(SyntaxRule):
    def __init__(self):
        self.NodeToken = NonTerm.AnonymousType

    def apply_ws(self, start, end):
        pos = start
        while pos < end:
            token = self.code.get_token(pos)
            if token == Tokens[',']:
                self.code.set_space_after(pos, '\n' if csharp_new_line_before_members_in_anonymous_types else ' ')
            pos+=1

    def check(self, s):
        if get_val(s, 0) == NonTerm.Block:
            if get_val(s, 1) == Tokens['new']:
                return 2
        return 0
