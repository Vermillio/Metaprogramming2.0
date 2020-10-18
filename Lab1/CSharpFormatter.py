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

        GenericRule(),
        IdentifierRule(),

        SwitchIndentRule(),

        SquareBracketsRule(),
        ParenthesesRule(),

        ObjectInitializerRule(),
        AnonymousTypeRule(),
    ]

    def beautify(self, lexer):
        all_tokens=[]
        token, str = lexer.nextToken()
        while token != Token.EndOfInput:
            all_tokens.append((token, str))
            token, str = lexer.nextToken()

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
                        print(rule)
                        print([s.__str__() for s in stack])
                        break
            pos+=1

        return token_processor.get_str()

lexer = CSharpLexer("""/*
 /*
 * C# Program to Perform Bubble Sort
 */

using System;
class bubblesort
{
        static void Main(string[] args)
        {
            int[] a = { 3, 2, 5, 4, 1 };
            int t;
            Console.WriteLine("The Array is : ");
            for (int i = 0; i < a.Length; i++)
            {
                Console.WriteLine(a[i]);
            }
            for (int j = 0; j <= a.Length - 2; j++)
            {
                for (int i = 0; i <= a.Length - 2; i++)
                {
                    if (a[i] > a[i + 1])
                    {
                        t = a[i + 1];
                        a[i + 1] = a[i];
                        a[i] = t;

                        switch () {
                        case 1:
                        a = 1;
                        break;
                        case 2: {a = 1;}break;
                        default: { a = 0;  }break;
                        }
                    }
                }
            }
            Console.WriteLine("The Sorted Array :");

            foreach (int aray in a)
                Console.Write(aray + " ");

            Console.ReadLine();
        }
    }
""")
formatter = CSharpFormatter()
s = formatter.beautify(lexer)
print(s)
