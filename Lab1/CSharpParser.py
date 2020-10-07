from CSharpLexer import *

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

# def copy_tree(root):
#     if not root:
#         return None
#     return ASTNode(root.Val, copy_tree(Left), copy_tree(Right))

class Rule:
    From = []
    To = None

    def __init__(From, To):
        self.From = from
        self.To = To

    def reduce(stack):
        for i in range(0, len(stack)):
            if stack[i].Val not in From[i]:
                return False

        TreeValues = stack[:len(From)]
        NewTree = ASTNode(To)
        for tv in TreeValues:
            NewTree.add_child(tv)
        stack = stack[len(From):]
        stack.insert(0, NewTree)




# switch identifier expression


class CSharpParser:

    stack = []
    rules = [
        Rule([ [Tokens['using']], [Tokens['whitespace']], [Identifier]], NonTerm.UsingDirective),
        Rule([ [NonTerm.Expression, NumericLiteral], [Tokens['+']], [NonTerm.Expression] ], NonTerm.Expression),
        Rule([ [NonTerm.Expression], [Tokens['?']], [NonTerm.Expression], [Tokens[':']], [NonTerm.Expression] ], NonTerm.TernaryOperator),
        Rule([ [Tokens['If']], [Tokens['whitespace']], [Tokens['(']], [NonTerm.Condition], [Tokens[')']], [Tokens['whitespace']], [Tokens['{']]  ], NonTerm.IfStatement),
     ]

    def buildAST(tokens):
#       tree = ASTNode(None, None, None)
        for token in tokens:
            stack.insert(0, ASTNode(token))
            for rule in rules:
                rule.reduce(stack)
