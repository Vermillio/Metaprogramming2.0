from KotlinLexer import KotlinLexer
import logging

class KotlinStyleChecker:

    def remove_whitespaces(self, tokens):
        return [t for t in tokens if t.token not in ["Whitespace", 'Newline']]

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

    def check_naming(self, tokens):
        prev = tokens[0]
        for token in tokens:
            if token.token == 'Identifier':
                if prev.token == 'Keyword':
                    if prev.str == 'package':
                        token.str = self.check_package_name(token)
                    elif prev.str == 'class':
                        token.str = self.check_class_name(token)

    def check_comments(self, tokens):
        for token in tokens:
            token[1] = self.check_multiline_comment(token)
        return tokens

    def fix(self, str, log_file=None):
        logging.basicConfig(filename=log_file, encoding='utf-8', level=logging.DEBUG)
        lexer = KotlinLexer(str)
        tokens=[]
        token_data = lexer.nextToken()
        while token_data.token != "EndOfInput" or token_data.token != "Error":
            tokens.append(token_data)
            token_data = lexer.nextToken()
        tokens = self.remove_whitespaces(tokens)
        tokens = self.check_comments(tokens)
        tokens = self.check_naming(tokens)
        return str
