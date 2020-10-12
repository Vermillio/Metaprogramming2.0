from CSharpLexer import *
from CSharpSyntaxRules import *



class CSharpParser:

    stack = []

    # rules = [
    #     SyntaxRule([ [Tokens['using']], [Tokens['whitespace']], [Identifier]], NonTerm.UsingDirective),
    #     SyntaxRule([Tokens['namespace'], [Tokens['whitespace']], [Identifier]], NonTerm.Namespace),
    #
    #     SyntaxRule([class_modifiers], NonTerm.ClassModifiersGroup),
    #     SyntaxRule([NonTerm.ClassModifiersGroup], [Tokens['whitespace']], [NonTerm.ClassModifiersGroup], NonTerm.ClassModifiersGroup),
    #     ClassDeclRule(),
    #     FuncDeclRule(),
    #     IfRule(),
    #     IfElseRule(),
    #     SwitchRule(),
    #     SwitchBodyRule(),
    #     CaseRule(),
    #     IdentifierRule(),
    #     AssignmentRule(),
    #     CallFuncOrMethodRule(),
    #
    #     # conditions and expressions
    #
    #     SyntaxRule([[Tokens['(']], [NonTerm.Condition], [Tokens[')']]], NonTerm.Condition),
    #     SyntaxRule([[Tokens['(']], [NonTerm.Expression], [Tokens[')']]], NonTerm.Expression),
    #
    #     SyntaxRule([[NonTerm.Condition, NonTerm.Expression], [Tokens[i] for i in RelationalOperators]+[Tokens[i] for i in LogicalOperators], [NonTerm.Condition, NonTerm.Expression]], NonTerm.Condition),
    #
    #     SyntaxRule([ [NonTerm.Expression, Literal, Identifier], [Tokens[i] for i in ArithmeticOperators]+[Tokens[i] for i in BitwiseOperators], [NonTerm.Expression, Literal, Identifier] ], NonTerm.Expression),
    #     SyntaxRule([ [NonTerm.Expression], [Tokens['?']], [NonTerm.Expression], [Tokens[':']], [NonTerm.Expression] ], NonTerm.TernaryOperator),
    #  ]

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
        token = lexer.nextToken()
        stack = []
        while token[0] != Token.EndOfInput:
            print(token[1])
            stack.insert(0, ASTNode(token[0]))
            token = lexer.nextToken()
            reduced = True
            while reduced:
                reduced = False
                for rule in self.rules:
                    stack, reduced = rule.reduce(stack)
                    if reduced:
                        print(rule)
                        print([s.__str__() for s in stack])
                        break
        return stack

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

parser = CSharpParser()

print(parser.buildAST(lexer))
