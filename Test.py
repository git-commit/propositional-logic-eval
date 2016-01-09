import unittest
import Lex
import Parse


class LexTest(unittest.TestCase):

    def test_lex(self):
        self.assertEqual(Lex.lex("test"), ["test"])
        self.assertEqual(Lex.lex("if (*p1-- == *p2++) then f() else g()"),
                        ["if", "(", "*", "p1", "--", "==", "*", "p2", "++", ")", "then", "f", "(", ")", "else", "g", "(", ")"])
        self.assertEqual(Lex.lex("((("), ["(", "(", "("])
        self.assertEqual(Lex.lex("if (*p1--55 == *p2++) then f() else g()"),
                        ["if", "(", "*", "p1", "--", "55", "==", "*", "p2", "++", ")", "then", "f", "(", ")", "else", "g", "(", ")"])
        self.assertEqual(Lex.lex("55 aa5"), ["55", "aa5"])

    def test_lexwhile(self):
        self.assertEqual(Lex.lexwhile(str.isalnum, "asfafsasf13((("), ("asfafsasf13", "((("))
        self.assertEqual(Lex.lexwhile(str.isalnum, "((("), ("", "((("))

class ParseTest(unittest.TestCase):
    def test_tokens(self):
        pass
        #self.assertEqual(Parse.createTokens(Lex.lex("true /\\ false")),
        #    [Parse.Token(Parse.typeVar, "true"), Parse.Token(Parse.typeDual, "/\\"), Parse.Token(Parse.typeVar, "false")])
        #self.assertEqual(Parse.createTokens(Lex.lex("~var")), [Parse.Token(Parse.typeSingle, "~"), Parse.Token(Parse.typeVar, "var")])

    def test_parse(self):
        parser = Parse.ParseTreeGenertor()
        print(parser.parse("b <=> (a <=> ~a)"))
