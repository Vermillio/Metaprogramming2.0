"""
    Basic token types and the standard tokens.
"""

class TokenType(tuple):
    parent = None

    def split(self):
        buf = []
        node = self
        while node is not None:
            buf.append(node)
            node = node.parent
        buf.reverse()
        return buf

    def __init__(self, *args):
        self.subtypes = set()

    def __contains__(self, val):
        return self is val or (
            type(val) is self.__class__ and
            val[:len(self)] == self
        )

    def __getattr__(self, val):
        if not val or not val[0].isupper():
            return tuple.__getattribute__(self, val)
        new = TokenType(self + (val,))
        setattr(self, val, new)
        self.subtypes.add(new)
        new.parent = self
        return new

    def __repr__(self):
        return 'Token' + (self and '.' or '') + '.'.join(self)

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

# Token = TokenType()
#
# Text = Token.Text
# Whitespace = Text.Whitespace
# Escape = Token.Escape
# Error = Token.Error
# Other = Token.Other
#
# # Common token types for source code
# Keyword = Token.Keyword
# Name = Token.Name
# Literal = Token.Literal
# String = Literal.String
# Number = Literal.Number
# Punctuation = Token.Punctuation
# Operator = Token.Operator
# Comment = Token.Comment
# CommentMultiline = Comment.CommentMultiline
#
# Generic = Token.Generic
#
# Token.Token = Token
# Token.String = String
# Token.Number = Number


def is_token_subtype(ttype, other):
    """
    Return True if ``ttype`` is a subtype of ``other``.
    """
    return ttype in other


def string_to_tokentype(s):
    if isinstance(s, TokenType):
        return s
    if not s:
        return Token
    node = Token
    for item in s.split('.'):
        node = getattr(node, item)
    return node
