from kotlin_style_check.KotlinLexer import KotlinLexer, TokenData
import os
import argparse
import fnmatch
import logging
import re

__version__ = "0.3"

class KotlinStyleChecker:
    def __init__(self):
        self.fixed_name_str = 'line {}: {} -> {} - Fixed {} name'
        self.logger = logging.getLogger('KotlinStyleCheckerLogger')

    ''' if this is not called then no logging happens '''
    def setup_logger(self, log_file, level=logging.INFO):
        logger = logging.getLogger('KotlinStyleCheckerLogger')
        logger.setLevel(level)
        formatter = logging.Formatter('%(message)s')
        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    def _log_name_fixed(self, line, old_str, new_str, log_name):
        if old_str != new_str:
            self.logger.info(self.fixed_name_str.format(line, old_str, new_str, 'package'))
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

    def _remove_whitespaces(self, tokens):
        return [t for t in tokens if t.token not in ["Whitespace", 'Newline']]

    def fix_multiline_comment(self, str, line):
        new_str = str if str[2] == '*' else str[:2] + '*' + str[2:]
        new_str = new_str if new_str[3] == '\n' else new_str[:3] + '\n' + new_str[3:]
        new_str = re.sub('\n[ \t]*\*?[ \t]?', '\n * ', new_str)
        new_str = new_str if new_str[-3] == '\n' else new_str[:-2]+'\n'+new_str[-2:]
        if '@param' in new_str or '@return' in new_str:
            self.logger.warning("line {}: Avoid using @param and @return tags in comments.".format(line))
        if str != new_str:
            self.logger.info('line {}: Fixed comment marking\n\n{}\n->\n{}\n\n'.format(line, str, new_str))
        return str, new_str

    def fix_class_name(self, token):
        return self._log_name_fixed(token.line, token.str, self.to_camel_case(token.str, first_capital=True), 'class')

    def fix_package_name(self, token):
        return self._log_name_fixed(token.line, token.str, self.to_camel_case(token.str), 'package')

    def fix_function_name(self, token):
        if not (token.str[0] == '`' and token.str[-1] == '`'):
            str = self.to_camel_case(token.str)
        elif token.str[1:-1] not in Keywords:
                self.logger.info('line {}: {} - Backticks are used in method name and method name is not a reserved keyword. Refactoring is recommended.'.format(token.line, token.str))
        return self._log_name_fixed(token.line, token.str, str, 'function')

    def fix_test_method_name(self, token):
        if not (token.str[0] == '`' and token.str[-1] == '`'):
            return self._log_name_fixed(token.line, token.str, self.to_camel_case(token.str, leave_underscores=True), 'test method')
        return token.str, token.str

    def fix_const_var_name(self, token):
        str = self.to_scream_snake_case(token.str)
        return self._log_name_fixed(token.line, token.str, str, 'const variable')

    def fix_var_name(self, token):
        return self._log_name_fixed(token.line, token.str, self.to_camel_case(token.str), 'variable')

    def fix_private_var_name(self, token):
        return self._log_name_fixed(token.line, token.str, '_'+self.to_camel_case(token.str), 'private variable')

    def check_comments(self, tokens, replacements):
        for token in tokens:
            if token.token == 'CommentMultiline':
                str_from, str_to = self.fix_multiline_comment(token.str, token.line)
                if str_from != str_to:
                    replacements[str_from] = str_to

    def check_naming(self, tokens, replacements):
        str_from, str_to, level = "", "", 0
        level = 0
        private_var_indices = []
        for i in range(len(tokens)):
            level += 1 if tokens[i].str == '{' else -1 if tokens[i].str == '}' else 0
            if level < 0:
                self.logger.warning('line {}: } is used without opening {')
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
                    while str_to in list(replacements.values()):
                        str_to += "_"
                    replacements[str_from] = str_to
        for i in private_var_indices:
            str_from, str_to = self.fix_private_var_name(tokens[i]) if self.to_camel_case(tokens[i].str) in list(replacements.values()) else self.fix_var_name(tokens[i])
            if str_from != str_to and str_from not in replacements.keys():
                while str_to in list(replacements.values()):
                    str_to += "_"
                replacements[str_from] = str_to

    def _replace(self, strings, replacements):
        return [ replacements[s] if s in replacements.keys() else s for s in strings ]

    def fix(self, file_contents, log_files):
        if not file_contents or not log_files or len(file_contents) == 0 or len(file_contents) != len(log_files):
            return None
        file_tokens, replacements = [], {}
        for file_content, log_file in zip(file_contents, log_files):
            self.setup_logger(log_file)
            tokens = KotlinLexer(file_content).get_tokens(file_content)
            cleared_tokens = self._remove_whitespaces(tokens)
            self.check_comments(cleared_tokens, replacements)
            self.check_naming(cleared_tokens, replacements)
            file_tokens += [tokens]
        return [''.join(self._replace([token.str for token in tokens], replacements)) for tokens in file_tokens]

    def fix_in_files(self, input_path):
        file_contents = []
        file_names = []
        if os.path.isdir(input_path):
            for dir, _, files in os.walk(input_path):
                rel_dir = os.path.relpath(dir, input_path)
                kotlin_files = fnmatch.filter(files, "*.kt")
                for file in kotlin_files:
                    file_name = os.path.join(dir, file)
                    with open(file_name) as f:
                        file_contents.append(f.read())
                        file_names.append(file_name)
        elif os.path.isfile(input_path):
            with open(input_path) as f:
                file_contents.append(f.read())
                file_names.append(input_path)
        else:
            return
        file_contents = self.fix(file_contents, log_files=[f[:-3]+"_fixing.log" for f in file_names])
        for file_name,  file_content in zip(file_names, file_contents):
            with open(file_name, 'w') as f:
                f.write(file_content)

    def run_tests(self, log_file):
        self.setup_logger(log_file)
        file_contents = ["""class C {
            private val elementList = mutableListOf<Element>()
            val ElementList: List<Element>
                 get() = elementList
        }"""]
        expected = """
        class C {
            private val _elementList = mutableListOf<Element>()
            val elementList: List<Element>
                 get() = _elementList
        }
        """
        got = KotlinStyleChecker().fix(file_contents, log_files=["tests.log"])[0]
        if expected != got:
            self.logger.info("One of tests failed")

def main():
    parser = argparse.ArgumentParser(description="Specify input path (file or dir)")
    parser.add_argument("--input_path", help="path to check Kotlin code conventions", required=True)
    args = parser.parse_args()
    run_tests('tests.log')
    KotlinStyleChecker().fix_in_files(args.input_path)

if __name__ == "__main__":
    main()