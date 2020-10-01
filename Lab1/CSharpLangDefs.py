ArithmeticOperators = ['+','-','*','/','%']
LogicalOperators = ['||', '&&', '!']
RelationalOperators = ['>=', '<=', '==', '!=', '<', '>']
AssignmentOperators = ['+=', '-=', '=']
BitwiseOperators = ['&', '|', '~', '^', '>>', '<<']
IncrementOperators=['++', '--']
SpecialOperators=['is', 'sizeof', 'as', 'typeof', 'new', 'checked', 'unchecked', 'dot']

Operators = ArithmeticOperators + LogicalOperators + RelationalOperators + AssignmentOperators + BitwiseOperators + IncrementOperators + SpecialOperators

Punctuators = [';', ':', ',', '.', '(', ')', '[', ']', '{', '}']

Keywords = ['abstract',	'as', 'base',	'bool',
'break',	'byte',	'case',	'catch',
'char', 'checked',	'class', 'const',
'continue',	'decimal',	'default',	'delegate',
'do',	'double',	'else',	'enum',
'event',	'explicit',	'extern',	'false',
'finally',	'fixed', 'float',	'for',
'foreach',	'goto',	'if',	'implicit',
'in',	'int',	'interface',	'internal',
'is',	'lock',	'long',	'namespace',
'new',	'null',	'object',	'operator',
'out',	'override',	'params',	'private',
'protected',	'public',	'readonly',	'ref',
'return',	'sbyte',	'sealed',	'short',
'sizeof',	'stackalloc',	'static',	'string',
'struct',	'switch',	'this',	'throw',
'true',	'try',	'typeof',	'uint',
'ulong',	'unchecked',	'unsafe',	'ushort',
'using',	'virtual',	'void',	'volatile',
'while']

ContextualKeywords = [
'add',	'alias',	'ascending',
'async',	'await',	'by',
'descending',	'dynamic',	'equals',
'from',	'get',	'global',
'group',	'into',	'join',
'let',	'nameof',	'notnull',
'on',	'orderby',	'partial (type)',
'partial (method)',	'remove',	'select',
'set',	'unmanaged', '(generic type constraint)',	'value',
'var',	'when', '(filter condition)',	'where', '(generic type constraint)',
'where', '(query clause)',	'yield']
