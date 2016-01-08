#!/usr/bin/python3


def main():
    print(lex("if (*p1-- == *p2++) then f() else g()"))


def lexwhile(typeFunction, inp):
    index = 0
    while typeFunction(inp[index]):
        index += 1
    return (inp[:index], inp[index:])


def lex(inp):
    tokens = []
    rest = inp
    while len(rest) > 1:
        rest = lexwhile(str.isspace, rest)[1]  # remove all spaces
        c, cs = rest[0], rest[1:]
        typefun = get_type_function(c)
        token, rest = lexwhile(typefun, cs)
        tokens.append(c + token)
    return tokens


def get_type_function(c):
    if (str.isalnum(c)):
        return str.isalnum
    if (is_symbol(c)):
        return is_symbol
    return lambda x: False


def is_symbol(c):
    return c in "~`!@#$%^&*-+=|\\:;<>.?/"


def parse(inp):
    pass

if __name__ == '__main__':
    main()
