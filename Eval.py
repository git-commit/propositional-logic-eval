import Parse
import Logic

def eval(formula, v):
    '''
    Evaluate the formula with the given valuation
    '''
    if (hasattr(formula, "type")):  # houston we have a leaf
        if formula.type is Parse.typeConstBool:
            return formula.value
        elif formula.type is Parse.typeVar:
            return valuation(formula.value, v)
    else:  # operator
        token = formula[0]
        op_fun = Logic.get_op(token.value)


        if token.type is Parse.typeDual:
            left = formula[1]
            right = formula[2]
            return op_fun(eval(left, v), eval(right, v))
        elif token.type is Parse.typeSingle:
            return op_fun(eval(formula[1], v))


def atoms(formula):
    '''
    Get a list of all atoms
    '''
    if (hasattr(formula, "type")):
        atoms_set = set()
        if formula.type is Parse.typeVar:
            atoms_set.add(formula.value)
        return atoms_set
    else:
        atoms_set = set()
        for a in formula:
            atoms_set.update(atoms(a))
        return atoms_set


def valuation(var, valuations):
    return valuations[var]


def all_valuations(atoms):
    num_valuations = 2 ** len(atoms)

    for i in range(0, num_valuations):
        b_str = bin(i)[2:].zfill(len(atoms))
        atom_value_dict = dict()
        i = 0
        for a in atoms:
            atom_value_dict[a] = bool(int(b_str[i]))
            i += 1
        yield atom_value_dict


def on_all_valuations(formula):
    '''
    Use eval for all valuations. Do all return true?
    '''
    formula_tree = Parse.parse(formula)

    for v in all_valuations(atoms(formula_tree)):
        if not eval(formula_tree, v):
            return False

    return True


def tautology(formula):
    return on_all_valuations(formula)


def unsatisfiable(formula):
    return tautology("~(" + formula + ")")


def satisfiable(formula):
    return not unsatisfiable(formula)


def entails(f1, f2):
    return tautology("(%s)=>(%s)" % (f1, f2))
