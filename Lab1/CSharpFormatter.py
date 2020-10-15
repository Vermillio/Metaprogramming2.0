import os
import argparse
import fnmatch
from config import *
from CSharpLangDefs import *

# newline after each line

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

    def get_str(self, node):
        return self.AllTokens[node.Pos][1]

    def add_indent(self, ws, indent):
        for i in reversed(range(len(ws))):
            if ws[i]=='\n':
                ws = ws[:i+1]+indent+ws[i+1:]
        return ws

    def remove_redundant_whitespaces(self):
        pass
    #    for token in AllTokens:
    #        if token == Token.Whitespace

    def beautify(self, template=None):
        self.template = template
        self.SyntaxTree, self.AllTokens = self.parser.buildAST(self.lexer)
        self.remove_redundant_whitespaces()

        print("TRAVERSE")
        return self.traverse(self.SyntaxTree, 0)

    def traverse(self, node, indent):
        indent_str = indent_size * indent * ('\t' if indent_style == 'tab' else ' ')
        if len(node.Children) == 0:
            # leaf
            return (self.add_indent(node.BeforeWs, indent_str) if node.BeforeWs != None else '') + self.get_str(node) + (self.add_indent(node.AfterWs, indent_str) if node.AfterWs != None else '')

        # todo: make separate rule for this
        if node == NonTerm.UsingBlock:
            node.Children = node.Children.sort(key = lambda c: -1 if self.get_str(c.Children[1].Children[0]) == 'System' else 1  )

        traversed = [ self.traverse(c, indent+1 if node.Val in [NonTerm.BlockContent, NonTerm.SwitchBody, NonTerm.CaseContent] else indent) for c in node.Children ]

        return (self.add_indent(node.BeforeWs, indent_str) if node.BeforeWs != None else '') + ''.join(traversed) + (self.add_indent(node.AfterWs, indent_str) if node.AfterWs != None else '')

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
