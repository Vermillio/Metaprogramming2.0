from KotlinLexer import KotlinLexer
import logging

class KotlinStyleChecker:

    def remove_whitespaces(self, tokens):
        return [t for t in tokens if t[0] not in ["Whitespace", 'Newline']]

    def check_multiline_comment(self, token):
        if token[0] != 'CommentMultiline':
            return token[1]
        str=token[1]
        line=token[2]
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

    def check_naming(self, tokens):
        prev = tokens[0]
        for token in tokens:
            if token[0] == 'Identifier':
                if prev[0] == 'Keyword':
                    if prev[1] == 'package':
                        token[1] = self.check_package_name(token)
                    elif prev[1] == 'class':
                        token[1] = self.check_class_name(token)

    def check_comments(self, tokens):
        for token in tokens:
            token[1] = self.check_multiline_comment(token)
        return tokens

    def fix(self, str, log_file=None):
        logging.basicConfig(filename=log_file, encoding='utf-8', level=logging.DEBUG)
        lexer = KotlinLexer(str)
        tokens=[]
        token, token_str = lexer.nextToken()
        while token != "EndOfInput":
            tokens.append((token, token_str))
            token, token_str = lexer.nextToken()
        tokens = self.remove_whitespaces(tokens)
        tokens = self.check_comments(tokens)
        tokens = self.check_naming(tokens)
        return str
