#!/usr/bin/python3
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

Token = collections.namedtuple('Token', ['type', 'value'])


def token_generator(tokens):
    for t in tokens:
        if t == t_lpar:
            n_tok = Token(t_lpar, t_lpar)
        elif t == t_rpar:
            n_tok = Token(t_rpar, t_rpar)
        elif any(t == op for op in [t_bic, t_imp, t_or, t_and]):
            n_tok = Token(typeDual, t)
        elif t == t_not:
            n_tok = Token(typeSingle, t)
        elif str.isalnum(t):
            n_tok = Token(typeVar, t)
        else:
            raise SyntaxError("Invalid token: " + t)
        yield n_tok


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
            op = self.tok.value
            right = self.expr()
            exprval = (op, exprval, right)

        return exprval

    def atom(self):
        'atom ::= (VAR | true | false) | ( expr ) | ¬ expr'

        if self._accept(typeVar):
            return self.tok.value
        elif self._accept(t_lpar):
            exprval = self.expr()
            self._expect(t_rpar)
            return exprval
        elif self._accept(typeSingle):
            exprval = ('~', self.expr())
            return exprval
        else:
            raise SyntaxError('Expected VAR, ( or ~')
