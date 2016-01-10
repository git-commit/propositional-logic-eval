import unittest
import Lex
import Parse
import Eval


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
        #self.assertEquals(parser.parse("b <=> (a <=> ~a)"), ('<=>', 'b', ('<=>', 'a', ('~', 'a'))))
        self.assertEquals(parser.parse("~((a => ((b /\\ c) \\/ d \\/ e) <=> true))"), (Parse.str_to_tok('~'), (Parse.str_to_tok("=>"), Parse.str_to_tok("a"), (Parse.str_to_tok("<=>"), (Parse.str_to_tok("\\/"), (Parse.str_to_tok("/\\"), Parse.str_to_tok("b"), Parse.str_to_tok("c")), (Parse.str_to_tok("\\/"), Parse.str_to_tok("d"),  Parse.str_to_tok("e"))), Parse.str_to_tok("true")))))
        self.assertEquals(Parse.parse("true"), (Parse.str_to_tok("true")))

    def test_parse_priority(self):
        parser = Parse.ParseTreeGenertor()

        #self.assertEquals(parser.parse("a <=> b => c"), ("=>", ("<=>", "a", "b"), "c"))


class EvalTest(unittest.TestCase):
    def test_atoms(self):
        parser = Parse.ParseTreeGenertor()
        self.assertEquals(Eval.atoms(parser.parse("~((a => ((b /\\ c) \\/ d \\/ e) <=> f))")), {'a', 'b', 'c', 'd', 'e', 'f'})
        self.assertEquals(Eval.atoms(parser.parse("~((a => ((b /\\ c) \\/ d \\/ e) <=> true))")), {'a', 'b', 'c', 'd', 'e'})

    def test_eval_by_def(self):
        self.assertFalse(Eval.eval(Parse.parse("a \\/ b"), {"a": False, "b": False}))
        self.assertTrue(Eval.eval(Parse.parse("a \\/ b"), {"a": False, "b": True}))
        self.assertTrue(Eval.eval(Parse.parse("a \\/ b"), {"a": True, "b": False}))
        self.assertTrue(Eval.eval(Parse.parse("a \\/ b"), {"a": True, "b": True}))
        self.assertFalse(Eval.eval(Parse.parse("a \\/ a"), {"a": False}))
        self.assertTrue(Eval.eval(Parse.parse("a \\/ a"), {"a": True}))

        self.assertFalse(Eval.eval(Parse.parse("a /\\ b"), {"a": False, "b": False}))
        self.assertFalse(Eval.eval(Parse.parse("a /\\ b"), {"a": False, "b": True}))
        self.assertFalse(Eval.eval(Parse.parse("a /\\ b"), {"a": True, "b": False}))
        self.assertTrue(Eval.eval(Parse.parse("a /\\ b"), {"a": True, "b": True}))
        self.assertFalse(Eval.eval(Parse.parse("a /\\ a"), {"a": False}))
        self.assertTrue(Eval.eval(Parse.parse("a /\\ a"), {"a": True}))

        self.assertFalse(Eval.eval(Parse.parse("a => b"), {"a": True, "b": False}))
        self.assertTrue(Eval.eval(Parse.parse("a => b"), {"a": True, "b": True}))
        self.assertTrue(Eval.eval(Parse.parse("a => b"), {"a": False, "b": True}))
        self.assertTrue(Eval.eval(Parse.parse("a => b"), {"a": False, "b": False}))

        self.assertTrue(Eval.eval(Parse.parse("a <=> b"), {"a": False, "b": False}))
        self.assertFalse(Eval.eval(Parse.parse("a <=> b"), {"a": False, "b": True}))
        self.assertFalse(Eval.eval(Parse.parse("a <=> b"), {"a": True, "b": False}))
        self.assertTrue(Eval.eval(Parse.parse("a <=> b"), {"a": True, "b": True}))



    def test_eval_complex(self):
        self.assertFalse(Eval.eval(Parse.parse("a /\\ ~(a <=> a)"), {"a": False}))
        self.assertFalse(Eval.eval(Parse.parse("a /\\ ~(a <=> a)"), {"a": True}))

        self.assertFalse(Eval.eval(Parse.parse("(Smoke => Fire) => (~Smoke => ~Fire)"), {"Smoke": False, "Fire": False}))
        self.assertFalse(Eval.eval(Parse.parse("(Smoke => Fire) => (~Smoke => ~Fire)"), {"Smoke": False, "Fire": True}))
        self.assertTrue(Eval.eval(Parse.parse("(Smoke => Fire) => (~Smoke => ~Fire)"), {"Smoke": True, "Fire": False}))
        self.assertTrue(Eval.eval(Parse.parse("(Smoke => Fire) => (~Smoke => ~Fire)"), {"Smoke": True, "Fire": True}))

        self.assertTrue(Eval.eval(Parse.parse("a /\\ (b \\/ c)"), {"a": True, "b": False, "c": True}))
        self.assertFalse(Eval.eval(Parse.parse("(a /\\ b) \\/ c"), {"a": True, "b": False, "c": False}))


    def test_eval_simple(self):
        self.assertTrue(Eval.eval(Parse.parse("true"), {}))
        self.assertFalse(Eval.eval(Parse.parse("false"), {}))

    def test_all_valuations(self):
        self.assertEquals(list(Eval.all_valuations(["a", "b"])), [
            {"a": False, "b": False},
            {"a": False, "b": True},
            {"a": True, "b": False},
            {"a": True, "b": True},
            ])

        self.assertEquals(len(list(Eval.all_valuations(["a", "b"]))), 2 ** 2)
        self.assertEquals(len(list(Eval.all_valuations(["a", "b", "c"]))), 2 ** 3)
        self.assertEquals(len(list(Eval.all_valuations(["a", "b", "c", "d"]))), 2 ** 4)

    def test_tautology(self):
        self.assertFalse(Eval.tautology("a /\\ b"))
        self.assertTrue(Eval.tautology("a <=> a"))
        self.assertFalse(Eval.tautology("a <=> b"))

    def test_satisfiable(self):
        self.assertTrue(Eval.satisfiable("a /\\ b"))
        self.assertFalse(Eval.satisfiable("a /\\ ~a"))

class ExerciseTest(unittest.TestCase):

    def test_exercise41(self):
        self.assertTrue(Eval.entails("False", "True"))
        self.assertFalse(Eval.entails("True", "False"))
