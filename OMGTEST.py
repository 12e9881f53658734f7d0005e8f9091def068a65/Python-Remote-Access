def getsilly(s1, s2):
    print(s1, s2)


def ok(fn):
    a = fn.__code__.co_varnames[:fn.__code__.co_argcount]
    return a

print(ok(getsilly))