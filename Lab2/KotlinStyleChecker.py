from Lab2.KotlinLexer import KotlinLexer, TokenData
import logging

def to_camel_case(str, first_capital=False, leave_underscores=False):
    str = reversed([str[i].upper()
                if (i>0 and ((str[i].isupper() and str[i-1].islower())) or not str[i-1].isalpha())
            else str[i].lower()
                if str[i].isalpha()
            else str[i]
                for i in reversed(range(len(str)))])
    str = [ s for s in str if s.isalnum() or (leave_underscores == True and s=='_')]
    if str[0].isalpha():
            str[0] = str[0].upper() if first_capital else str[0].lower()
    return ''.join(str)

class KotlinStyleChecker:

    def __init__(self):
        self.fixed_name_str = 'line {}: {} -> {} - Fixed {} name'

    def remove_whitespaces(self, tokens):
        new_tokens = []
        whitespaces = []
        for i in range(len(tokens)):
            if tokens[i].token not in ["Whitespace", 'Newline']:
                new_tokens.append(tokens[i])
            else:
                whitespaces.append((tokens[i], i))
        return new_tokens, whitespaces

    def return_whitespaces(self, tokens, whitespaces):
        for ws in whitespaces:
            tokens = tokens[:ws[1]] + [ws[0]] + tokens[ws[1]:]
        return tokens

    def check_multiline_comment(self, token):
        if token.token != 'CommentMultiline':
            return token.str
        str=token.str
        line=token.line
        fixed = False
        if str[2] != '*':
            str = str[:2] + '*' + str[2:]
            fixed = True
        for i in range(len(str)):
            if str[i] == '\n' and str[i+1] != '*':
                str = str[:i+1] + '*' + str[i+1:]
                fixed = True
        if str.contains('@param') or str.contains('@return'):
            logging.warning("line {}: avoid using @param and @return tags.".format(line))
        if fixed:
            logging.debug('line {}: Fixed comment marking'.format(line))
        return str

    def check_class_name(self, token):
        str = to_camel_case(token.str, first_capital=True)
        if str != token.str:
            logging.debug(self.fixed_name_str.format(token.line, token.str, str, 'class'))
        return str

    def check_package_name(self, token):
        str = to_camel_case(token.str)
        if str != token.str:
            logging.debug(self.fixed_name_str.format(token.line, token.str, str, 'package'))
        return str

    def check_function_name(self, token):
        if not (token.str[0] == '`' and token.str[-1] == '`'):
            str = to_camel_case(token.str)
        else:
            if token.str[1:-1] in Keywords:
                # we can use backticks
                pass
            else:
                # need to do something
                logging.debug('line {}: {} - Backticks are used in method name and method name is not a reserved keyword. Refactoring is recommended.'.format(token.line, token.str))
                pass
        if str != token.str:
            logging.debug(self.fixed_name_str.format(token.line, token.str, str, 'function'))
        return str

    def check_test_method_name(self, token):
        if not (token.str.first() == '`' and token.str.last() == '`'):
            str = to_camel_case(token.str, leave_underscores=True)
            if str != token.str:
                logging.debug(self.fixed_name_str.format(token.line, token.str, str, 'test method'))
        return str

    def check_comments(self, tokens):
        for token in tokens:
            token.str = self.check_multiline_comment(token)
        return tokens

    def check_naming(self, tokens):
        for i in range(len(tokens)):
            token = tokens[i]
            if token.token == 'Identifier':
                if i > 0 and tokens[i-1].token == 'Keyword':
                    if tokens[i-1].str == 'package':
                        token.str = self.check_package_name(token)
                    elif tokens[i-1].str == 'class':
                        token.str = self.check_class_name(token)
                    elif tokens[i-1].str == 'fun':
                        if i > 2 and tokens[i-2].str == 'Test' and tokens[i-3].str == '@':
                            token.str = self.check_test_method_name(token)
                        else:
                            token.str = self.check_function_name(token)
        return tokens

    def fix(self, file_contents, log_file=None):
        logging.basicConfig(filename=log_file, level=logging.DEBUG)

        for str in file_contents:
            lexer = KotlinLexer(str)
            tokens=[]
            token_data = lexer.nextToken()
            while token_data.token != "EndOfInput" and token_data.token != "Error":
                print(token_data)
                tokens.append(token_data)
                token_data = lexer.nextToken()
            replacements = []

            tokens, whitespaces = self.remove_whitespaces(tokens)
            replacements += self.check_comments(tokens)
            replacements += check_naming(tokens)
            return self.replace_in_files(file_contents, replacements)
            #tokens = self.check_comments(tokens)
            #tokens = self.check_naming(tokens)
            #tokens = self.return_whitespaces(tokens, whitespaces)
            #return ''.join([token.str for token in tokens])
