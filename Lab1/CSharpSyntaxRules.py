import itertools
from ASTNode import *
from CSharpTokenProcessor import *

class SyntaxRule:
    NodeToken = None
    token_processor = None

    def __init__(self, From, NodeToken):
        self.NodeToken = NodeToken

    def set_token_processor(self, token_processor):
        self.token_processor = token_processor

    def resolve_whitespaces(self, node):
        pass

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

        self.resolve_whitespaces(NewTree)
        return stack, True

class ClassDeclRule(SyntaxRule):
    def __init__(self):
        self.NodeToken = NonTerm.ClassDecl

    def resolve_whitespaces(self, node):
        start = node.Start
        end = node.End
        for pos in range(start, end-1):
            token = self.token_processor.get_token(pos)
            if token == Tokens[':']:
                self.token_processor.set_space_after(pos, ' ' if Settings.csharp_space_after_colon_in_inheritance_clause else '')
                self.token_processor.set_space_before(pos, ' ' if Settings.csharp_space_before_colon_in_inheritance_clause else '')
            else:
                self.token_processor.set_space_after(pos, ' ')

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

    def resolve_whitespaces(self, node):
        start = node.Start
        end = node.End
        for pos in range(start, end):
            token = self.token_processor.get_token(pos)
            if token == Tokens['(']:
                self.token_processor.set_space_before(pos, ' ' if Settings.csharp_space_between_method_declaration_name_and_open_parenthesis else '')
                if self.token_processor.get_token(pos+1) == Tokens[')']:
                    self.token_processor.set_space_after(pos, ' ' if Settings.csharp_space_between_method_declaration_empty_parameter_list_parentheses else '')
                else:
                    self.token_processor.set_space_after(pos, ' ' if Settings.csharp_space_between_method_declaration_parameter_list_parentheses else '')
            elif token == Tokens[')']:
                if self.token_processor.get_token(pos-1)==Tokens['(']:
                    self.token_processor.set_space_before(pos, ' ' if Settings.csharp_space_between_method_declaration_empty_parameter_list_parentheses else '')
                    pass
                else:
                    self.token_processor.set_space_before(pos, ' ' if Settings.csharp_space_between_method_declaration_parameter_list_parentheses else '')

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

    def resolve_whitespaces(self, node):
        start = node.Start
        end = node.End
        self.token_processor.set_space_after(start, '')
        self.token_processor.set_space_before(end-1, '')

    def check(self, s):
        pos=0
        if get_val(s, pos) == Tokens['>'] and get_val(s, pos+1) in [Identifier] and get_val(s, pos+2) == Tokens['<']:
            return pos+3
        return 0

class SwitchIndentRule(SyntaxRule):
    def __init__(self):
         self.NodeToken = NonTerm.SwitchBlock

    def resolve_whitespaces(self, node):
        start = node.Start
        end = node.End
        switch_content = node.Children[1].Children
        for node in switch_content[1:-1]:
            token = node.Val
            if not Settings.csharp_indent_switch_labels:
                for i in range(node.Start, node.End):
                    self.token_processor.dec_indent(pos)
            if ( Settings.csharp_indent_case_contents_when_block and token == NonTerm.Block
                or Settings.csharp_indent_case_contents and token not in [NonTerm.Block, Tokens['case'], Tokens['default']]):
                for i in range(node.Start, node.End):
                    self.token_processor.inc_indent(node.Start)
            if token in [Tokens['case'], Tokens['default']]:
                self.token_processor.set_space_before(node.Start, '\n')
            elif token in [Tokens[':']]:
                self.token_processor.set_space_before(node.Start, '')
                self.token_processor.set_space_after(node.Start, '\n')
            # elif token in [Tokens['break']]


    def check(self, s):
        pos=0
        if get_val(s, 0) == NonTerm.Block and get_val(s, 1) == NonTerm.Switch:
            return 2
        return 0

class IdentifierRule(SyntaxRule):
    def __init__(self):
        self.NodeToken = NonTerm.ComplexIdentifier

    def resolve_whitespaces(self, node):
        start = node.Start
        end = node.End
        for pos in range(start, end-1):
            self.token_processor.set_space_after(pos, '')

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

    def resolve_whitespaces(self, node):
        start = node.Start
        end = node.End
        open_parentheses_pos = node.Children[1].Start
        self.token_processor.set_space_before(open_parentheses_pos, ' ' if Settings.csharp_space_between_method_call_name_and_opening_parenthesis else '')
        for pos in range(start, end):
            token = self.token_processor.get_token(pos)
            if token == Tokens['(']:
                self.token_processor.set_space_after(pos, ' ' if Settings.csharp_space_between_method_call_parameter_list_parentheses else '')
            elif token == Tokens[')']:
                self.token_processor.set_space_before(pos, ' ' if Settings.csharp_space_between_method_call_parameter_list_parentheses else '')
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

    def resolve_whitespaces(self, node):
        start = node.Start
        end = node.End
        is_single_line_block = True
        for pos in range(start, end-1):
            space = self.token_processor.get_space_after(pos)
            if '\n' in space:
                is_single_line_block = False

        for pos in range(start+1, end-1):
            token = self.token_processor.get_token(pos)
            next_token = self.token_processor.get_token(pos+1)
            if token == NonTerm.EmptyLine:
                is_single_line_block = False
            elif token == Identifier and next_token == Tokens[':']:
                if Settings.csharp_indent_labels == 'flush_left':
                    self.token_processor.set_indent(pos, -1)
                elif Settings.csharp_indent_labels == 'one_less_than_current':
                    self.token_processor.dec_indent(pos)
                self.token_processor.set_space_after(pos, '')
                self.token_processor.set_space_after(pos+1, '\n')

        if is_single_line_block and Settings.csharp_preserve_single_line_blocks:
            self.token_processor.set_space_before(start, ' ') # todo: separate rule for {};
            self.token_processor.set_space_after(start, ' ')
            self.token_processor.set_space_before(end-1, ' ')
            #self.token_processor.set_space_after(end-1, '')
        else:
            self.token_processor.set_space_after(start, '\n')
            self.token_processor.set_space_before(end-1, '\n')
            self.token_processor.set_space_after(end-1, '\n')

        # indent
        if Settings.csharp_indent_block_contents:
            for pos in range(start+1, end-1):
                self.token_processor.inc_indent(pos)

        if Settings.csharp_indent_braces:
            self.token_processor.inc_indent(start)
            self.token_processor.inc_indent(end-1)

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

#template
class ControlFlowRule(SyntaxRule):
    def __init__(self):
        pass

    def resolve_whitespaces(self, node):
        start = node.Start
        end = node.End
        self.token_processor.set_space_after(start, ' ' if Settings.csharp_space_after_keywords_in_control_flow_statements else '')
        keyword = self.token_processor.get_token(start)
        if keyword == Tokens['for']:
            for pos in range(start+1, end):
                token = self.token_processor.get_token(pos)
                if token == Tokens[';']:
                    self.token_processor.set_space_before(pos, ' ' if Settings.csharp_space_before_semicolon_in_for_statement else '')
                    self.token_processor.set_space_after(pos, ' ' if Settings.csharp_space_after_semicolon_in_for_statement else '')
        self.token_processor.set_space_after(end-1, '\n')
        token = self.token_processor.get_token(end)
        if token != None and token != Tokens['{']:
            self.token_processor.inc_indent(end)

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

    def resolve_whitespaces(self, node):
        start = node.Start
        end = node.End
        self.token_processor.set_space_after(start, ' ' if Settings.csharp_space_between_parentheses else '')
        self.token_processor.set_space_before(end-1, ' ' if Settings.csharp_space_between_parentheses else '')

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

    def resolve_whitespaces(self, node):
        start = node.Start
        end = node.End
        if self.token_processor.get_space_before(start) != '\n':
            self.token_processor.set_space_before(start, ' ' if Settings.csharp_space_before_open_square_brackets else '')
        if end == start+2:
            self.token_processor.set_space_after(start, ' ' if Settings.csharp_space_between_empty_square_brackets else '')
        else:
            self.token_processor.set_space_after(start, ' ' if Settings.csharp_space_between_square_brackets else '')
            self.token_processor.set_space_before(end-1, ' ' if Settings.csharp_space_between_square_brackets else '')
        if self.token_processor.get_token(start+1) == Tokens['assembly']:
            if self.token_processor.get_token(start+2) == Tokens[':']:
                self.token_processor.set_space_after(end-1, '\n')


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

    def resolve_whitespaces(self, node):
        start = node.Start
        end = node.End
        for pos in range(start, end):
            token = self.token_processor.get_token(pos)
            if token == Tokens[',']:
                self.token_processor.set_space_after(pos, '\n' if Settings.csharp_new_line_before_members_in_object_initializers else ' ')

    def check(self, s):
        pos = 0
        if get_val(s, pos) == NonTerm.Block:
            pos+=1
            if get_val(s, pos) == NonTerm.Parentheses:
                pos+=1
            if get_val(s, pos) == NonTerm.Generic:
                pos+=1
            if get_val(s, pos) == Identifier:
                if get_val(s, pos+1) == Tokens['new']:
                    return pos+1
        return 0

class AnonymousTypeRule(SyntaxRule):
    def __init__(self):
        self.NodeToken = NonTerm.AnonymousType

    def resolve_whitespaces(self, node):
        start = node.Start
        end = node.End
        for pos in range(start, end):
            token = self.token_processor.get_token(pos)
            if token == Tokens[',']:
                self.token_processor.set_space_after(pos, '\n' if Settings.csharp_new_line_before_members_in_anonymous_types else ' ')

    def check(self, s):
        if get_val(s, 0) == NonTerm.Block:
            if get_val(s, 1) == Tokens['new']:
                return 2
        return 0

class CastRule(SyntaxRule):
    def __init__(self):
        self.NodeToken = NonTerm.Cast

    def resolve_whitespaces(self, node):
        start = node.Start
        end = node.End
        self.token_processor.set_space_after(start, ' ' if Settings.csharp_space_after_cast else '')

    def check(self, s):
        if get_val(s, 0) in [Identifier, NonTerm.ComplexIdentifier]:
            if get_val(s, 1) == NonTerm.Parentheses:
                return 2
        return 0


class QueryExpressionRule(SyntaxRule):
    def __init__(self):
        self.NodeToken = NonTerm.Expression

    def resolve_whitespaces(self, node):
        start = node.Start
        end = node.End
        for pos in range(start, end):
            token = self.token_processor.get_token(pos)
            if token in [Tokens['from'], Tokens['where'], Tokens['select'], Tokens['group'], Tokens['let'], Tokens['orderby']]:
                self.token_processor.set_space_before(pos, '\n' if Settings.csharp_new_line_between_query_expression_clauses else ' ')

    def check(self, s):
        pos=0
        if get_val(s, 0) in [Tokens['group'], Tokens['select']]:
            pos+=1
            checked = True
            while not pos >= len(s) and not get_val(s, pos) == Tokens[';']:
                if get_val(s, pos) == Tokens['in'] and get_val(s, pos+1) == NonTerm.Identifier and get_val(s, pos+2) == Tokens['from']:
                    return pos+3
                pos+=1
        return 0
