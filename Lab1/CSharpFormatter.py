import os
import argparse
import fnmatch
from config import *
from CSharpLangDefs import *
from CSharpLexer import *
from CSharpSyntaxRules import *

class CSharpFormatter:
    rules = [
        UsingRule(),
        ClassDeclRule(),
        MethodDeclRule(),
        MethodCallRule(),
        SimpleBlockRule(),
        ControlFlowRule(),
        SwitchIndentRule(),
        GenericRule(),
        IdentifierRule(),
        SquareBracketsRule(),
        ParenthesesRule(),
        ObjectInitializerRule(),
        AnonymousTypeRule(),
        CastRule(),
        QueryExpressionRule(),
    ]

    def beautify(self, str, log = True):
        lexer = CSharpLexer(str)
        all_tokens=[]
        token, token_str = lexer.nextToken()
        while token != Token.EndOfInput:
            all_tokens.append((token, token_str))
            token, token_str = lexer.nextToken()
        token_processor = CSharpTokenProcessor(all_tokens)
        token_processor.check_single_tokens()
        for rule in self.rules:
            rule.set_token_processor(token_processor)
        pos = 0
        stack = []
        while pos < len(token_processor.tokens):
            stack.insert(0, ASTNode(token_processor.get_token(pos), pos, pos+1))
            reduced = True
            while reduced:
                reduced = False
                for rule in self.rules:
                    stack, reduced = rule.reduce(stack)
                    if reduced:
                        break
            pos+=1

        #self.organize_usings(token_processor, stack)
        return token_processor.get_full_str()

    def organize_usings(self, stack):
        usings = [s for s in stack if s.Val == NonTerm.Using]
        stack_without_usings = [s for s in stack if s.Val != NonTerm.Using]
        formatted_usings = []
        if dotnet_sort_system_directives_first:
            formatted_usings = [s for s in stack if token_processor.get_str(usings[i].Start+1) == 'System' ]
            usings = [s for s in stack if token_processor.get_str(usings[i].Start+1) != 'System' ]

        if dotnet_separate_import_directive_groups:
            groups = {}
            for i in range(len(usings)):
                group = token_processor.get_str(usings[i].Start+1)
                if not groups[group]:
                    groups[group] = [i]
                else:
                    groups[group] += [i]
