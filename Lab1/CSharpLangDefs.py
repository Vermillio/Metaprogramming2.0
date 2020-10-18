from Tokens import *

Token = TokenType()
NonTerm = TokenType()

Keyword = Token.Keyword
Identifier = Token.Identifier
Literal = Token.Literal
Operator = Token.Operator
Punctuator = Token.Punctuator

Comment = Token.Comment
CommentMultiline = Comment.CommentMultiline

NumericLiteral = Literal.NumericLiteral
CharacterLiteral = Literal.CharacterLiteral
BooleanLiteral = Literal.BooleanLiteral
StringLiteral = CharacterLiteral.StringLiteral
IntegerLiteral = NumericLiteral.IntegerLiteral
NullLiteral = Literal.NullLiteral

Literals = [NumericLiteral, CharacterLiteral, BooleanLiteral, StringLiteral, IntegerLiteral, NullLiteral]

ArithmeticOperators = ['+','-','*','/','%']
LogicalOperators = ['||', '&&', '!']
RelationalOperators = ['>=', '<=', '==', '!=', '<', '>']
AssignmentOperators = ['+=', '-=', '=']
BitwiseOperators = ['&', '|', '~', '^', '>>', '<<']
IncrementOperators=['++', '--']
SpecialOperators=['is', 'sizeof', 'as', 'typeof', 'new', 'checked', 'unchecked', 'dot', '?']

Operators = ArithmeticOperators + LogicalOperators + RelationalOperators + AssignmentOperators + BitwiseOperators + IncrementOperators + SpecialOperators
BinaryOperators = ArithmeticOperators + LogicalOperators + RelationalOperators + AssignmentOperators + BitwiseOperators + SpecialOperators

Punctuators = [';', ':', ',', '.', '(', ')', '[', ']', '{', '}']

Types = ['bool', 'double', 'decimal','float', 'int', 'long', 'short', 'sbyte', 'string', 'uint','ulong', 'ushort','void']

Keywords = ['abstract',	'as', 'base',
'break',	'byte',	'case',	'catch',
'char', 'checked',	'class', 'const',
'continue',	'default',	'delegate',
'do',	'else',	'enum',
'event',	'explicit',	'extern',	'false',
'finally',	'fixed',	'for',
'foreach',	'goto',	'if',	'implicit',
'in',	'interface',	'internal',
'is',	'lock',	'namespace',
'new',	'object',	'operator',
'out',	'override',	'params',	'private',
'protected',	'public',	'readonly',	'ref',
'return',	'sealed',
'sizeof',	'stackalloc',	'static',
'struct',	'switch',	'this',	'throw',
'true',	'try',	'typeof',	'unchecked',	'unsafe',
'using',	'virtual',	'volatile',
'while']+Types

ContextualKeywords = [
'add',	'alias',	'ascending',
'async',	'await',	'by',
'descending',	'dynamic',	'equals',
'from',	'get',	'global',
'group',	'into',	'join',
'let',	'nameof',	'notnull',
'on',	'orderby',	'partial',
'remove',	'select',
'set',	'unmanaged', '(generic type constraint)',	'value',
'var',	'when', '(filter condition)',	'where', '(generic type constraint)',
'where', '(query clause)',	'yield']

AllTokens = Operators+Punctuators+Keywords+ContextualKeywords
Tokens = dict.fromkeys(AllTokens)
for i in range(len(AllTokens)):
    Tokens[AllTokens[i]]=Token.__getattr__('A'+str(i))

access_modifiers = [Tokens['public'], Tokens['internal'], Tokens['private'], Tokens['protected']]

class_modifiers = [Tokens['public'], Tokens['internal'], Tokens['abstract'], Tokens['const'], Tokens['extern'], Tokens['partial'], Tokens['sealed'], Tokens['static']]

whitespace_tokens = [Token.Tab, Token.Whitespace, Token.UnknownWhitespace]
