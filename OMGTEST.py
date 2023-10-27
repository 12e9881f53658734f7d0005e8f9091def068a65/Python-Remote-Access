def getsilly(e):
    print("LOL " + e)

import types
funcs = [f for f in globals().values() if callable(f)]

for f in funcs:
    print(f.__name__)