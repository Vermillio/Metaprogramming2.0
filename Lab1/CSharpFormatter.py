import os
import argparse
import fnmatch
from config import *

# newline after each line

whitespace_table = [
    ( [NonTerm.File], ['\n\n'] ),
    ( [NonTerm.UsingBlock], ['\n'] ),
    ( [NonTerm.UsingStatement], [' ', '\n'] ),
    ( [NonTerm.Block], ['\n','\n'] ),
    [Operators, ' ', ' '],


]

def search_whitespace_table(token):
    for item in whitespace_table:
        if token in item[0]:
            return item[1], item[2]
    return None, None

class CSharpFormatter:
    lexer = None
    parser = None
    template = None
    result = None

    def __init__(self, lexer, parser):
        self.lexer=lexer
        self.parser=parser

    def get_str(node):
        return self.AllTokens[node.Pos][1]

    def remove_redundant_whitespaces(self):
        for token in AllTokens:
            if token == Token.Whitespace

    def beautify(self, template=None):
        self.template = template
        self.SyntaxTree, self.AllTokens = parser.BuildAST(lexer)
        remove_redundant_whitespaces()

        result = traverse(self.SyntaxTree, 0)

        return ''.join(result)

    def traverse(self, node, indent):
        if len(node.Children) == 0:
            # leaf
            return self.get_str(node)

        if node == NonTerm.UsingBlock:
            node.Children = node.Children.sort(key = lambda c: -1 if self.get_str(c.Children[1].Children[0]) == 'System' else 1  )

        traversed = [ traverse(c, indent+1 if node.Val == NonTerm.Block else indent) for c in node.Children ]
        found_whitespace_vals = next(x[1] for x in whitespace_table if x[0] == node.Val )
        if found_whitespace_vals:
            whitespaces = node.replace_whitespaces(found_whitespace_vals)

        for i in range(len(whitespaces)):
            if whitespaces[i] == '\n':
                whitespaces[i] = '\n' + indent_size * indent * '\t' if indent_style == 'tab' else ' '

        for i in range(1, len(whitespaces)+1):
            traversed.insert(2*i-1, whitespaces[i-1])
        return ''.join(traversed)


#        for c in node.Children:
#return handlers[node.Val].apply()
#        return before_ws + ''.join(  ) + after_ws

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
