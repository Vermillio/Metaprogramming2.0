from CSharpLexer import *
from CSharpSyntaxRules import *

class ASTNode:
    Val = None
    Children = []

    def __init__(self, Val):
        self.Val = Val

    def add_child(Child):
        if not isinstance(Child, ASTNode):
            return False
        Children.append(Child)
        return True

    def get_child(ind):
        return Children[ind]



class CSharpParser:

    stack = []

    # rules = {
    #     'default' : [
    #
    #     ],
    #     'class_decl' : [
    #
    #     ]
    # }

    rules = [
        SyntaxRule([ [Tokens['using']], [Tokens['whitespace']], [Identifier]], NonTerm.UsingDirective),
        SyntaxRule([Tokens['namespace'], [Tokens['whitespace']], [Identifier]], NonTerm.Namespace),

        # finished

#        SyntaxRule([NonTerm.ClassModifiersGroup, [Tokens['whitespace']], NonTerm.ClassDecl),

        SyntaxRule([class_modifiers], NonTerm.ClassModifiersGroup),
        SyntaxRule([NonTerm.ClassModifiersGroup], [Tokens['whitespace']], [NonTerm.ClassModifiersGroup], NonTerm.ClassModifiersGroup),
        ClassDeclRule(),
        FuncDeclRule(),
        IfRule(),
        IfElseRule(),
        SwitchRule(),
        SwitchBodyRule(),
        CaseRule(),
        IdentifierRule(),
        AssignmentRule(),
        CallFuncOrMethodRule(),

        # conditions and expressions

        SyntaxRule([[Tokens['(']], [NonTerm.Condition], [Tokens[')']]], NonTerm.Condition),
        SyntaxRule([[Tokens['(']], [NonTerm.Expression], [Tokens[')']]], NonTerm.Expression),

        SyntaxRule([[NonTerm.Condition, NonTerm.Expression], [Tokens[i] for i in RelationalOperators]+[Tokens[i] for i in LogicalOperators], [NonTerm.Condition, NonTerm.Expression]], NonTerm.Condition),

        SyntaxRule([ [NonTerm.Expression, Literal, Identifier], [Tokens[i] for i in ArithmeticOperators]+[Tokens[i] for i in BitwiseOperators], [NonTerm.Expression, Literal, Identifier] ], NonTerm.Expression),
        SyntaxRule([ [NonTerm.Expression], [Tokens['?']], [NonTerm.Expression], [Tokens[':']], [NonTerm.Expression] ], NonTerm.TernaryOperator),
     ]

    def buildAST(tokens):
#       tree = ASTNode(None, None, None)
        for token in tokens:
            stack.append(ASTNode(token))
            reduced = True
            while reduced:
                reduced = False
                for rule in rules:
                    if rule.reduce(stack):
                        reduced = True
