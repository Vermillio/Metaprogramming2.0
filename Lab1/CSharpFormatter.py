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
    ]

    def beautify(self, str, log = True):
        lexer = CSharpLexer(str)
        all_tokens=[]
        token, token_str = lexer.nextToken()
        while token != Token.EndOfInput:
            all_tokens.append((token, token_str))
            token, token_str = lexer.nextToken()
        if log:
            print(1)
        token_processor = CSharpTokenProcessor(all_tokens)
        token_processor.check_single_tokens()
        if log:
            print(2)
        for rule in self.rules:
            rule.set_token_processor(token_processor)
        pos = 0
        stack = []
        while pos < len(token_processor.tokens):
            if log:
                print(3)
            stack.insert(0, ASTNode(token_processor.get_token(pos), pos, pos+1))
            reduced = True
            while reduced:
                reduced = False
                for rule in self.rules:
                    if log:
                        print(rule)
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



# str = """/*
#  /*
#  * C# Program to Perform Bubble Sort
#  */
#
# using System;
# class bubblesort
# {
#         static void Main(string[] args)
#         {
#             int[] a = { 3, 2, 5, 4, 1 };
#             int t = a ? 3 : 1;
#             Console.WriteLine("The Array is : ");
#             for (int i = 0; i < a.Length; i++)
#             {
#                 Label1:
#                 Console.WriteLine(a[i]);
#             }
#             for (int j = 0; j <= a.Length - 2; j++)
#             {
#                 for (int i = 0; i <= a.Length - 2; i++)
#                 {
#                     if (a[i] > a[i + 1])
#                     {
#                         t = a[i + 1];
#                         a[i + 1] = a[i];
#                         a[i] = t;
#                         Label2:
#                         switch () {
#                         case 1:
#                         a = 1;
#                         break;
#                         case 2: {a = 1;}break;
#                         default: { a = 0;  }break;
#                         }
#                     }
#                 }
#             }
#             Console.WriteLine("The Sorted Array :");
#
#             foreach (int aray in a)
#                 Console.Write(aray + " ");
#
#             Console.ReadLine();
#         }
#     } """
# formatter = CSharpFormatter()
# s = formatter.beautify(str)
# print(s)
