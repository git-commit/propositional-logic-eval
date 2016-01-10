#!/usr/bin/python3

import Eval


def main():
    # Problem 4.1.
    print('''
Problem 4.1. Use the function entails to check whether the following
entailment is true or not.
1. False |= True
2. True |= False
3. (A ∧ B) |= (A ⇔ B)
4. (A ⇔ B) |= A ∨ B
5. (A ⇔ B) |= ¬A ∨ B

Solutions:
1. %s
2. %s
3. %s
4. %s
5. %s
''' % (
        Eval.entails("False", "True"),  # 1. False |= True
        Eval.entails("True", "False"),  # 2. True |= False
        Eval.entails("a /\\ b", "a <=> b"),  # 3. (A ∧ B) |= (A ⇔ B)
        Eval.entails("a <=> b", "a \\/ b"),  # 4. (A ⇔ B) |= A ∨ B
        Eval.entails("a <=> b", "~a \\/ b")  # 5. (A ⇔ B) |= ¬A ∨ B
    ))


    # Problem 4.2.2
    f1 = "Smoke => Smoke"
    f2 = "(Smoke => Fire) => (~Smoke => ~Fire)"
    f3 = "Smoke \\/ Fire\\/ ~Fire"
    f4 = "(Fire => Smoke) /\\ Fire /\\ ~Smoke"


    print(
    '''
Problem 4.2.2 Use the function tautology, satisfiable, unsatisfiable
to check whether the following formulae is tautology, satisfiable, or unsat-
isfiable. Compare the output with the result from your pencil-and-paper
derivation.
1. Smoke ⇒ Smoke
2. (Smoke ⇒ Fire) ⇒ (¬Smoke ⇒ ¬Fire)
3. Smoke ∨ Fire ∨ ¬Fire
4. (Fire ⇒ Smoke) ∧ Fire ∧ ¬Smoke

Solutions:
1. %s

2. %s

3. %s

4. %s
    ''' % (
        ex42(f1),
        ex42(f2),
        ex42(f3),
        ex42(f4)
        ))

    # Exercise 4.2.3
    bsays = "b <=> (a <=> ~a)"
    csays = "c <=> ~b"
    kb = "(%s) /\\ (%s) " % (bsays, csays)

    print(
'''
Problem 4.2.3
Represent what B says with your parser.

bsays = parse "b <=> (a <=> ~a)"

where parse is your parser implementation. Do the same with what C says.

csays = parse "c <=> ~b"

Construct a knowledge base —kb of type Formula— by performing conjunc-
tion of what B and C says. By using the function entails, check whether
the knowledge base entails whether A is a knight. Check also whether it
entails whether A is a knave. Perform these checks for B and C as well.

Solutions:
%s
%s
%s
%s
%s
%s
'''
        % (
    "KB |= a  = " + str(Eval.entails(kb, "a")),
    "KB |= ~a = " + str(Eval.entails(kb, "~a")),
    "KB |= b  = " + str(Eval.entails(kb, "b")),
    "KB |= ~b = " + str(Eval.entails(kb, "~b")),
    "KB |= c  = " + str(Eval.entails(kb, "c")),
    "KB |= ~c = " + str(Eval.entails(kb, "~c"))
    ))

def ex42(f):
    s = ""
    if Eval.satisfiable(f):
        s += "satisfiable "
    if Eval.unsatisfiable(f):
        s += "unsatisfiable "
    if Eval.tautology(f):
        s += "tautology"

    return s + "\n(satisfiable: %s, unsatisfiable %s, tautology: %s)" % (Eval.satisfiable(f), Eval.unsatisfiable(f), Eval.tautology(f))


if __name__ == '__main__':
    main()
