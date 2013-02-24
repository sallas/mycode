def sub(a, b):
    if b == 0:
        return a
    else:
        return sub(a, b-1) - 1

def slowMod(a, b):
    if a < b:
        return a
    else:
        return slowMod(a -b, b)
