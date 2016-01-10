'''
Logic operations
'''


def op_and(l, r):
    return l and r


def op_or(l, r):
    return l or r


def op_bicoditional(l, r):
    return l == r


def op_implication(l, r):
    return not (l and not r)


def op_not(r):
    return not r

op_map = {
    "<=>": op_bicoditional,
    "=>": op_implication,
    "\\/": op_or,
    "/\\": op_and,
    "~": op_not,
}


def get_op(op_string):
    return op_map[op_string]
