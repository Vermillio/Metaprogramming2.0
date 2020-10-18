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

    def remove_double_whitespaces(self, tokens):
        pos = 0
        while pos < len(tokens)-1:
            if tokens[pos][0] in whitespace_tokens+[Token.Newline] and tokens[pos+1][0] in whitespace_tokens:
                del tokens[pos+1]
            elif tokens[pos][0] in whitespace_tokens and tokens[pos+1][0] == Token.Newline:
                del tokens[pos]
            else:
                pos+=1
        return tokens

    def split_whitespaces(self, tokens):
        pos=0
        new_tokens = []
        whitespaces = [' ']
        while pos < len(tokens):
            if tokens[pos][0] == Token.Newline:
                if pos+1 < len(tokens) and tokens[pos+1][0] == Token.Newline:
                    whitespaces[-1]='\n'
                    new_tokens.append((Token.EmptyLine, ""))
                    whitespaces.append('\n')
                    pos+=2
                else:
                    pos+=1
            elif tokens[pos][0] not in whitespace_tokens:
                new_tokens.append(tokens[pos])
                whitespaces.append(' ')
                pos+=1
            else:
                whitespaces[-1]=' '
                pos+=1
        return new_tokens, whitespaces

    def beautify(self, lexer):
        all_tokens=[]
        token, str = lexer.nextToken()

        while token != Token.EndOfInput:
            all_tokens.append((token, str))
            token, str = lexer.nextToken()

        tokens, whitespaces = self.split_whitespaces(self.remove_double_whitespaces(all_tokens))
        code = Code(tokens, whitespaces)
        for rule in self.rules:
            rule.code = code

        self.check_single_tokens(code)

        pos = 0
        stack = []
        while pos < len(tokens):
            print(tokens[pos][0])
            stack.insert(0, ASTNode(tokens[pos][0], pos, pos+1))
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

        return code.get_str()

    def check_single_tokens(self, code):
        for pos in range(len(code.tokens)):
            token = code.get_token(pos)
            if token == Tokens[',']:
                code.set_space_before(pos, ' ' if csharp_space_before_comma else '')
                code.set_space_after(pos, ' ' if csharp_space_after_comma else '')
            elif token == Tokens['.']:
                code.set_space_before(pos, ' ' if csharp_space_before_dot else '')
                code.set_space_after(pos, ' ' if csharp_space_after_dot else '')
            elif token in [Tokens[i] for i in BinaryOperators]:
                code.set_space_before(pos, ' ' if csharp_space_around_binary_operators else '')
                code.set_space_after(pos, ' ' if csharp_space_around_binary_operators else '')
            elif token == Tokens['catch']:
                code.set_space_before(pos, '\n' if csharp_new_line_before_catch else ' ')
            elif token == Tokens['finally']:
                code.set_space_before(pos, '\n' if csharp_new_line_before_finally else ' ')
            elif token == Tokens['else']:
                code.set_space_before(pos, '\n' if csharp_new_line_before_else else ' ')
            elif token == Tokens['{']:
                code.set_space_before(pos, '\n' if csharp_new_line_before_open_brace else ' ')
            elif token == Tokens[';']:
                code.set_space_before(pos, '')
                code.set_space_after(pos, '\n')



def parse_template(path):
    template = None
    with open(path) as f:
        f.read()
    return template


if __name__ == "__main__":
    formatter = CSharpFormatter()

    parser = argparse.ArgumentParser(description="Specify input and output!")
    parser.add_argument("--input_path", help="path to format", required=True)
    parser.add_argument("--output_path", help="path to save result", required=True)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", help="file", action='store_true')
    group.add_argument("-d", "--directory", help="directory", action='store_true')
    group.add_argument("-p", "--project", help="project", action='store_true')

    parser.add_argument("--template", help="path to template file")
    args = parser.parse_args()

    template_path = None if not args.template else args.template
    template = parse_template(template_path)

    if args.file:
        with open(args.input_path) as fi:
            str = fi.read()
            beautified_str = formatter.beautify(str, template)
            out_file = args.output_path
            if not os.path.exists(os.path.dirname(out_file)):
                try:
                    os.makedirs(os.path.dirname(out_file))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            with open(out_file, 'w') as fo:
                fo.write(beautified_str)
    elif args.directory:
        for dir, _, files in os.walk(args.input_path):
            rel_dir = os.path.relpath(dir, args.input_path)
            for file in fnmatch.filter(files, "*.cs"):
                rel_file = os.path.join(rel_dir, file)
                with open(os.path.join(dir, file)) as f:
                    str = f.read()
                    beautified_str = formatter.beautify(str, template)
                    out_file = os.path.join(args.output_path, rel_file)
                    if not os.path.exists(os.path.dirname(out_file)):
                        try:
                            os.makedirs(os.path.dirname(out_file))
                        except OSError as exc: # Guard against race condition
                            if exc.errno != errno.EEXIST:
                                raise
                    with open(out_file, 'w') as fo:
                        fo.write(beautified_str)

lexer = CSharpLexer("""namespace System.Main.Complex {
public class IAbstractFactory<T>
{
    void main<T> ( int a, S b ) {
        main();
    }
}
}""")


lexer = CSharpLexer("""/*
 * C# Program to Perform Bubble Sort
 */

if (a[i] > a[i + 1])
{
    t = a[i + 1];
    a[i + 1] = a[i];
    a[i] = t;
}
""")
s = CSharpFormatter().beautify(lexer)
print(s)
