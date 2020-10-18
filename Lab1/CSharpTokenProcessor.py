from CSharpLangDefs import *
from config import *

def apply_indent(str, indent):
    indent_str = indent_size * indent * ('\t' if indent_style == 'tab' else ' ') if indent >= 0 else None
    return str + indent_str if str == '\n' and indent_str else str

class CSharpTokenProcessor:
    tokens=[]
    whitespaces=[]
    indents=[]
    comments = []

    def __init__(self, tokens):
        self.tokens, self.whitespaces, self.comments = self._split_whitespaces_comments(self._remove_double_whitespaces(tokens))
        self.indents=[0]*len(self.tokens)

    def get_token(self, i):
        if i >= len(self.tokens):
            return None
        return self.tokens[i][0]

    def get_str(self, i):
        if i >= len(self.tokens):
            return None
        return self.tokens[i][1]

    def index(self, token, start, end):
        for i in range(start, end):
            if self.get_token(i) == token:
                return i
        return -1

    def set_space_after(self, i, ws):
        if ws != None:
            self.whitespaces[i+1] = ws

    def set_space_before(self, i, ws):
        if ws != None:
            self.whitespaces[i] = ws

    def get_space_before(self, i):
        return self.whitespaces[i]

    def get_space_after(self, i):
        return self.whitespaces[i+1]

    def set_indent(self, i, indent):
        if self.indents[i] >= 0:
            self.indents[i] = indent

    def inc_indent(self, i):
        if self.indents[i] >= 0:
            self.indents[i]+=1

    def dec_indent(self, i):
        if self.indents[i] >= 0:
            self.indents[i]-=1

    def get_full_str(self):
        s = [apply_indent(self.tokens[i][1], self.indents[i]) for i in range(len(self.tokens))]
        for i in range(0, len(self.indents)):
            s.insert(2*i, apply_indent(self.whitespaces[i], self.indents[i]))
        for comment, comment_str, i in self.comments:
            s = s[:i] + [comment_str] + s[i:]
        if insert_final_newline:
            s+=['\n']
        return ''.join(s)

    def _remove_double_whitespaces(self, tokens):
        pos = 0
        while pos < len(tokens)-1:
            if tokens[pos][0] in whitespace_tokens+[Token.Newline] and tokens[pos+1][0] in whitespace_tokens:
                del tokens[pos+1]
            elif tokens[pos][0] in whitespace_tokens and tokens[pos+1][0] == Token.Newline:
                del tokens[pos]
            else:
                pos+=1
        return tokens

    def _split_whitespaces_comments(self, tokens):
        pos=0
        new_tokens = []
        whitespaces = ['']
        comments = []
        whitespace_set = False
        skip_whitespace = False
        while pos < len(tokens):
            if tokens[pos][0] == Token.Newline:
                if pos+1 < len(tokens) and tokens[pos+1][0] == Token.Newline:
                    if not skip_whitespace:
                        whitespaces[-1]='\n'
                        skip_whitespace = False
                    new_tokens.append((Token.EmptyLine, ""))
                    whitespaces.append('\n')
                    pos+=1
                    whitespace_set = True
            elif tokens[pos][0] in [Token.Comment, Token.CommentMultiline]:
                if pos+1 < len(tokens) and tokens[pos+1][0] in whitespace_tokens+[Token.Newline]:
                    comments.append((tokens[pos][0], tokens[pos][1]+tokens[pos+1][1], len(new_tokens)+len(whitespaces) - 0 if whitespace_set else 1))
                    skip_whitespace = True
                else:
                    comments.append((tokens[pos][0], tokens[pos][1], len(new_tokens)+len(whitespaces) - 0 if whitespace_set else 1))
            elif tokens[pos][0] not in whitespace_tokens:
                new_tokens.append(tokens[pos])
                whitespaces.append(' ')
                whitespace_set = False
            else:
                if not skip_whitespace:
                    whitespaces[-1]=' '
                    skip_whitespace = False
                whitespace_set = True
            pos+=1
        return new_tokens, whitespaces, comments

    def check_single_tokens(self):
        for pos in range(len(self.tokens)):
            token = self.get_token(pos)
            if token == Tokens[',']:
                self.set_space_before(pos, ' ' if csharp_space_before_comma else '')
                self.set_space_after(pos, ' ' if csharp_space_after_comma else '')
            elif token == Tokens['.']:
                self.set_space_before(pos, ' ' if csharp_space_before_dot else '')
                self.set_space_after(pos, ' ' if csharp_space_after_dot else '')
            elif token in [Tokens[i] for i in BinaryOperators]:
                self.set_space_before(pos, ' ' if csharp_space_around_binary_operators else '')
                self.set_space_after(pos, ' ' if csharp_space_around_binary_operators else '')
            elif token == Tokens['catch']:
                self.set_space_before(pos, '\n' if csharp_new_line_before_catch else ' ')
            elif token == Tokens['finally']:
                self.set_space_before(pos, '\n' if csharp_new_line_before_finally else ' ')
            elif token == Tokens['else']:
                self.set_space_before(pos, '\n' if csharp_new_line_before_else else ' ')
            elif token == Tokens['{']:
                self.set_space_before(pos, '\n' if csharp_new_line_before_open_brace else ' ')
            elif token == Tokens[';']:
                self.set_space_before(pos, '')
                self.set_space_after(pos, '\n')
            elif token in [Tokens[i] for i in IncrementOperators]:
                self.set_space_before(pos, '')
                self.set_space_after(pos, '')
