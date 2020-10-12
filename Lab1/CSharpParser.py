from CSharpLexer import *
from CSharpSyntaxRules import *

class CSharpParser:

    stack = []
    rules = [
        SyntaxRule([ [Tokens[';']], [Identifier, NonTerm.ComplexIdentifier], [Tokens['using']]], NonTerm.UsingDirective),
        SyntaxRule([[NonTerm.Block],[Identifier],[Tokens['namespace']]], NonTerm.NamespaceBlock),
        IdentifierRule(),
        ArrayRule(),

        SimpleLineRule(),
        SimpleBlockRule(),
        ClassDeclRule(),
        FuncDeclRule(),
    ]

    def buildAST(self, lexer):
#       tree = ASTNode(None, None, None)
        token, str = lexer.nextToken()
        stack = []
        i = 0
        excluded = []
        while token != Token.EndOfInput:
            print(str)
            if token in [Tokens['whitespace'], Comment, CommentMultiline]:
                excluded.append([i, Token])
                continue

            stack.insert(0, ASTNode(token,str))
            token = lexer.nextToken()
            i+=1

            reduced = True
            while reduced:
                reduced = False
                for rule in self.rules:
                    stack, reduced = rule.reduce(stack)
                    if reduced:
                        print(rule)
                        print([s.__str__() for s in stack])
                        break
        return stack, excluded

lexer = CSharpLexer("""
using System;

namespace ArrayApplication {
   class MyArray {
      static void Main(string[] args) {
         int []  n = new int[10]; /* n is an array of 10 integers */

         /* initialize elements of array n */
         for ( int i = 0; i < 10; i++ ) {
            n[i] = i + 100;
         }

         /* output each array element's value */
         foreach (int j in n ) {
            int i = j-100;
            Console.WriteLine("Element[{0}] = {1}", i, j);
         }
         Console.ReadKey();
      }
   }
}
""")

parser = CSharpParser()

print(parser.buildAST(lexer))
