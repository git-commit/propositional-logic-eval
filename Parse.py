import Lex
import collections

# For a reference on recursive descent parsing in python I used the Python Cookbook 3rd Edition

# Token constants
t_bic = "<=>"
t_imp = "=>"
t_or = "\\/"
t_and = "/\\"
t_not = "~"
t_lpar = "("
t_rpar = ")"

# token types (without left and right parantheses)
typeDual = "OPDUAL"
typeSingle = "OPSINGLE"
typeVar = "VAR"
typeConstBool = "CONSTBOOL"

Token = collections.namedtuple('Token', ['type', 'value'])


def token_generator(tokens):
    for t in tokens:
        yield str_to_tok(t)


def str_to_tok(t):
        if t == t_lpar:
            return Token(t_lpar, t_lpar)
        elif t == t_rpar:
            return Token(t_rpar, t_rpar)
        elif any(t == op for op in [t_bic, t_imp, t_or, t_and]):
            return Token(typeDual, t)
        elif t == t_not:
            return Token(typeSingle, t)
        elif str.upper(t) == 'FALSE':
            return Token(typeConstBool, False)
        elif str.upper(t) == 'TRUE':
            return Token(typeConstBool, True)
        elif str.isalnum(t):
            return Token(typeVar, t)
        else:
            raise SyntaxError("Invalid token: " + t)


def parse(text):
    parser = ParseTreeGenertor()
    return parser.parse(text)


class ParseTreeGenertor:

    def parse(self, text):
        lexed = Lex.lex(text)

        self.tokens = token_generator(lexed)
        self.tok = None
        # Last symbol consumed
        self.nexttok = None
        # Next symbol tokenized
        self._advance()
        # Load first lookahead token
        return self.expr()

    def _advance(self):
        'Advance one token ahead'
        self.tok, self.nexttok = self.nexttok, next(self.tokens, None)

    def _accept(self, toktype):
        'Test and consume the next token if it matches toktype'
        if self.nexttok and self.nexttok.type == toktype:
            self._advance()
            return True
        else:
            return False

    def _expect(self, toktype):
        'Consume next token if it matches toktype or raise SyntaxError'
        if not self._accept(toktype):
            raise SyntaxError('Expected ' + toktype)

    '''
    Grammar rules (NOT present in the book)

    EBNF:   formula ::= atom { (⇔|⇒|∨|∧) formula }*
                  ::= ¬ formula

            atom ::= (VAR | true | false) | ( expr )
    '''

    def expr(self):
        '''
        expr ::= atom { (⇔|⇒|∨|∧) expr }* | ¬ expr
        '''
        exprval = self.atom()

        if self._accept(typeDual):
            op = self.tok
            right = self.expr()
            exprval = (op, exprval, right)

        return exprval

    def atom(self):
        'atom ::= (VAR | true | false) | ( expr ) | ¬ atom'

        if self._accept(typeVar) or self._accept(typeConstBool):
            return self.tok
        elif self._accept(t_lpar):
            exprval = self.expr()
            self._expect(t_rpar)
            return exprval
        elif self._accept(typeSingle):
            exprval = (str_to_tok('~'), self.atom())
            return exprval
        else:
            raise SyntaxError('Expected VAR, ( or ~')
