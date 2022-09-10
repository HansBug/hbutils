FIXED = 233


def m1():
    from mth import func2
    return func2() ** 2


def m2():
    from mth import func1, func2
    return (func2() + func1()) ** 3
