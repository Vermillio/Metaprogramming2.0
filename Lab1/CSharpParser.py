from CSharpLexer import *
from CSharpSyntaxRules import *

class CSharpParser:

    stack = []
    rules = [
        SyntaxRule([ [Tokens[';']], [Identifier, NonTerm.ComplexIdentifier], [Tokens['using']]], NonTerm.UsingDirective),
        SyntaxRule([[NonTerm.Block],[Identifier],[Tokens['namespace']]], NonTerm.NamespaceBlock),
        IdentifierRule(),
        ArrayRule(),

        ClassDeclRule(),
        FuncDeclRule(),
        IfRule(),
        IfElseRule(),
        SwitchRule(),
        SwitchBodyRule(),
        CaseRule(),
        ForLoopRule(),

        SimpleLineRule(),
        SimpleBlockRule(),

        # experimental
        SyntaxRule([[Tokens[')']],[NonTerm.Expression],[Tokens['(']]], NonTerm.Expression),
        SyntaxRule([[Tokens[')']],[NonTerm.Condition],[Tokens['(']]], NonTerm.Condition),
        SyntaxRule([ [NonTerm.Expression, Identifier,NonTerm.ComplexIdentifier]+Literals, [Tokens[i] for i in RelationalOperators]+[Tokens['is']], [NonTerm.Expression, Identifier,NonTerm.ComplexIdentifier]+Literals], NonTerm.Condition),
        SyntaxRule([ [NonTerm.Expression,Identifier,NonTerm.ComplexIdentifier]+Literals, [Tokens[i] for i in ArithmeticOperators]+[Tokens[i] for i in BitwiseOperators]+[Tokens[i] for i in LogicalOperators], [NonTerm.Expression, Literal,Identifier,NonTerm.ComplexIdentifier]+Literals ], NonTerm.Expression),
        SyntaxRule([ [NonTerm.Expression], [Tokens[':']], [NonTerm.Expression], [Tokens['?']], [NonTerm.Expression, NonTerm.Condition, NonTerm.Identifier] ], NonTerm.TernaryOperator),
    ]

    def buildAST(self, lexer):
#       tree = ASTNode(None, None, None)
        token, str = lexer.nextToken()
        print(token)
        stack = []
        all_tokens = []
        while token != Token.EndOfInput:
            all_tokens.append((token, str))
            if token in [Tokens['whitespace'], Comment, CommentMultiline, Token.NewLine]:
                token, str = lexer.nextToken()
                print(token)
                continue

            stack.insert(0, ASTNode(token,len(all_tokens)-1, None))
            token, str = lexer.nextToken()
            print(token)
            reduced = True
            while reduced:
                reduced = False
                for rule in self.rules:
                    stack, reduced = rule.reduce(stack)
                    if reduced:
                        print(rule)
                        print([s.__str__() for s in stack])
                        break
        return stack, all_tokens

lexer = CSharpLexer("""for(;;) { } """)


parser = CSharpParser()

print(parser.buildAST(lexer)[0])
