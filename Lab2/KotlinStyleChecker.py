from Lab2.KotlinLexer import KotlinLexer, TokenData
import logging
from sys import stdout

def setup_logger(log_file, level=logging.INFO):
    logging.getLogger().setLevel(level)
    formatter = logging.Formatter('%(message)s')
    handler = logging.StreamHandler(stdout)
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)

class KotlinStyleChecker:
    def __init__(self):
        self.fixed_name_str = 'line {}: {} -> {} - Fixed {} name'

    def log_name_fixed(self, line, old_str, new_str, log_name):
        if old_str != new_str:
            logging.info(self.fixed_name_str.format(line, old_str, new_str, 'package'))
        return old_str, new_str

    def to_camel_case(self, str, first_capital=False, leave_underscores=False):
        str = reversed([
                str[i].upper() if (i>0 and ((str[i].isupper() and str[i-1].islower())) or not str[i-1].isalpha())
                else str[i].lower() if str[i].isalpha()
                else str[i] for i in reversed(range(len(str))) ])
        str = [ s for s in str if s.isalnum() or (leave_underscores == True and s=='_')]
        if str[0].isalpha():
                str[0] = str[0].upper() if first_capital else str[0].lower()
        return ''.join(str)

    def to_scream_snake_case(self, str):
        for i in reversed(range(1,len(str))):
            if str[i].isupper() and str[i-1].islower():
                str = str[:i]+'_'+str[i:]
        return ''.join([s.upper() if s.isalpha() else s for s in str])

    def remove_whitespaces(self, tokens):
        return [t for t in tokens if t.token not in ["Whitespace", 'Newline']]

    def return_whitespaces(self, tokens, whitespaces):
        for ws in whitespaces:
            tokens = tokens[:ws[1]] + [ws[0]] + tokens[ws[1]:]
        return tokens

    def fix_multiline_comment(self, token):
        if token.token != 'CommentMultiline':
            return token.str, token.str
        str, line, fixed = token.str, token.line, false
        if str[2] != '*':
            str = str[:2] + '*' + str[2:]
            fixed = True
        for i in range(len(str)):
            if str[i] == '\n' and str[i+1] != '*':
                str = str[:i+1] + '*' + str[i+1:]
                fixed = True
        if '@param' in str or '@return' in str:
            logging.warning("line {}: Avoid using @param and @return tags in comments.".format(line))
        if fixed:
            logging.info('line {}: Fixed comment marking\n\n{}\n->\n{}\n\n'.format(line, token.str, str))
        return token.str, str

    def fix_class_name(self, token):
        return self.log_name_fixed(token.line, token.str, self.to_camel_case(token.str, first_capital=True), 'class')

    def fix_package_name(self, token):
        return self.log_name_fixed(token.line, token.str, self.to_camel_case(token.str), 'package')

    def fix_function_name(self, token):
        if not (token.str[0] == '`' and token.str[-1] == '`'):
            str = self.to_camel_case(token.str)
        elif token.str[1:-1] not in Keywords:
                logging.info('line {}: {} - Backticks are used in method name and method name is not a reserved keyword. Refactoring is recommended.'.format(token.line, token.str))
        return self.log_name_fixed(token.line, token.str, str, 'function')

    def fix_test_method_name(self, token):
        if not (token.str[0] == '`' and token.str[-1] == '`'):
            return self.log_name_fixed(token.line, token.str, self.to_camel_case(token.str, leave_underscores=True), 'test method')
        return token.str, token.str

    def fix_const_var_name(self, token):
        str = self.to_scream_snake_case(token.str)
        return self.log_name_fixed(token.line, token.str, str, 'const variable')

    def fix_var_name(self, token):
        return self.log_name_fixed(token.line, token.str, self.to_camel_case(token.str), 'variable')

    def fix_private_var_name(self, token):
        return self.log_name_fixed(token.line, token.str, '_'+self.to_camel_case(token.str), 'private variable')

    def check_comments(self, tokens, replacements):
        for token in tokens:
            str_from, str_to = self.fix_multiline_comment(token)
            if str_from != str_to:
                replacements[str_from] = str_to

    def check_naming(self, tokens, replacements):
        str_from, str_to, level = "", "", 0
        level = 0
        private_var_indices = []
        for i in range(len(tokens)):
            level += 1 if tokens[i].str == '{' else -1 if tokens[i].str == '}' else 0
            if level < 0:
                logging.warning('line {}: } is used without opening {')
            if i > 0 and tokens[i].token == 'Identifier' and tokens[i-1].token == 'Keyword':
                if tokens[i-1].str == 'package':
                    str_from, str_to = self.fix_package_name(tokens[i])
                elif tokens[i-1].str == 'class':
                    str_from, str_to = self.fix_class_name(tokens[i])
                elif tokens[i-1].str == 'fun' and i > 2 and tokens[i-2].str == 'Test' and tokens[i-3].str == '@':
                    str_from, str_to = self.fix_test_method_name(tokens[i])
                elif tokens[i-1].str == 'fun':
                        str_from, str_to = self.fix_function_name(tokens[i])
                elif tokens[i-1].str == 'val' and ((i<len(tokens)-1 and tokens[i+1] == '=' and level==0) or (i>2 and tokens[i-2].str == 'const')):
                    str_from, str_to = self.fix_const_var_name(tokens[i])
                elif tokens[i-1].str == 'val' and (i>2 and tokens[i-2].str == 'private'):
                    private_var_indices.append(i)
                elif tokens[i-1].str == 'val':
                    str_from, str_to = self.fix_var_name(tokens[i])
            if str_from != str_to and str_from not in replacements.keys():
                replacements[str_from] = str_to
        for i in private_var_indices:
            str_from, str_to = self.fix_private_var_name(tokens[i]) if self.to_camel_case(tokens[i].str) in replacements.keys() else self.fix_var_name(tokens[i])
            if str_from != str_to and str_from not in replacements.keys():
                replacements[str_from] = str_to

    def replace(self, strings, replacements):
        return [ replacements[s] if s in replacements.keys() else s for s in strings ]

    def fix(self, file_contents, log_files):
        file_tokens, replacements = [], {}
        for file_content, log_file in zip(file_contents, log_files):
            setup_logger(log_file)
            tokens = KotlinLexer(file_content).get_tokens(file_content)
            cleared_tokens = self.remove_whitespaces(tokens)
            self.check_comments(cleared_tokens, replacements)
            self.check_naming(cleared_tokens, replacements)
            file_tokens += [tokens]
        return [''.join(self.replace([token.str for token in tokens], replacements)) for tokens in file_tokens]
