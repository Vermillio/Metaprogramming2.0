from CSharpLexer import *
from CSharpSyntaxRules import *
from CSharpFormatter import *

class CSharpParser:

    stack = []
    # rules = [
    #     SyntaxRule([ [Tokens[';']], [Identifier, NonTerm.ComplexIdentifier], [Tokens['using']]], NonTerm.UsingDirective),
    #     SyntaxRule([[NonTerm.Block],[Identifier, NonTerm.ComplexIdentifier],[Tokens['namespace']]], NonTerm.NamespaceBlock),
    #     IdentifierRule(),
    #     ArrayRule(),
    #
    #     ClassDeclRule(),
    #     FuncDeclRule(),
    #     IfRule(),
    #     IfElseRule(),
    #     SwitchRule(),
    #     SwitchBodyRule(),
    #     CaseRule(),
    #     ForLoopRule(),
    #     WhileRule(),
    #
    #     SimpleLineRule(),
    #     SimpleBlockRule(),
    #
    #     # experimental
    #     SyntaxRule([[Tokens[')']],[NonTerm.Expression],[Tokens['(']]], NonTerm.Expression),
    #     SyntaxRule([[Tokens[')']],[NonTerm.Condition],[Tokens['(']]], NonTerm.Condition),
    #     SyntaxRule([ [NonTerm.Expression, Identifier,NonTerm.ComplexIdentifier]+Literals, [Tokens[i] for i in RelationalOperators]+[Tokens['is']], [NonTerm.Expression, Identifier,NonTerm.ComplexIdentifier]+Literals], NonTerm.Condition),
    #     SyntaxRule([ [NonTerm.Expression,Identifier,NonTerm.ComplexIdentifier]+Literals, [Tokens[i] for i in ArithmeticOperators]+[Tokens[i] for i in BitwiseOperators]+[Tokens[i] for i in LogicalOperators], [NonTerm.Expression, Literal,Identifier,NonTerm.ComplexIdentifier]+Literals ], NonTerm.Expression),
    #     SyntaxRule([ [NonTerm.Expression], [Tokens[':']], [NonTerm.Expression], [Tokens['?']], [NonTerm.Expression, NonTerm.Condition, NonTerm.Identifier] ], NonTerm.TernaryOperator),
    # ]

    rules = [   ClassDeclRule(),
                SimpleBlockRule(),
                BlockContentRule(),
                GenericRule(),
                MethodDeclRule(),
                IdentifierRule(),
                NamespaceRule(),
                SwitchRule(),
                SwitchBodyRule(),
                CaseRule(),
                ForLoopRule(),
                WhileLoopRule(),
                ]

    def buildAST(self, lexer):
        print_token = False
        token, str = lexer.nextToken()
        if print_token:
            print(token)
        stack = []
        all_tokens = []
        #whitespaces = []

        while token != Token.EndOfInput:
            all_tokens.append((token, str))
            if token in [Tokens['whitespace'], Comment, CommentMultiline, Token.NewLine]:
                token, str = lexer.nextToken()
                if print_token:
                    print(token)
                continue

            #formatted_tokens.

            current_node = ASTNode(token,len(all_tokens)-1)
            stack.insert(0, current_node)
            token, str = lexer.nextToken()
            if print_token:
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
        return stack[0], all_tokens

lexer = CSharpLexer("""namespace System.Main.Complex {
public class IAbstractFactory<T>
{
    void main<T> ( int a ) {

        do { for (;;) {}
        } while ();
    }
}
}""")


parser = CSharpParser()

formatter = CSharpFormatter(lexer, parser)
s = formatter.beautify(lexer)
print(s)

AST, AllTokens = parser.buildAST(lexer)
#print([AllTokens[i.Pos][1] for i in AST[0].Children if i.Pos != None])
#print(AST.display())
#print([AST[i].Val for i in range(len(AST))])
print(AllTokens)
