import timeit
from time import time


def naive():
    ss = []
    for i in range(1000):
        ss.append("a" + str(i) + "b" + str(i+1)\
            + str(i+2) + str(i+2) + str(i+2) + str(i+2) + str(i+2) + str(i+2) + str(i+2) + str(i+2) + str(i+2))
    return ss


def faster():
    ss = []
    for i in range(1000):
        ss.append("a%sb%s%s%s%s%s%s%s%s%s%s" % (str(i), str(i+1), str(i+2), str(i+2), str(i+2), str(i+2), str(i+2), str(i+2), str(i+2), str(i+2), str(i+2)))
    return ss


def n():
    t = time()
    s = 'lksdajflakjdsflku09uweoir'
    for x in range(30):
        ss = s[:int(len(s)/16)]
        s += ss
        s += ss
        s += ss
        s += ss
        s += ss
        
        s += ss
        s += ss
        s += ss
        s += ss
        s += ss
    print(len(s))
    print('duration:', time()-t)


def f():
    t = time()
    s = 'lksdajflakjdsflku09uweoir'
    for x in range(30):
        ss = s[:int(len(s)/16)]
        s = "".join([s,
                     ss,
                     ss,
                     ss,
                     ss,
                     ss,

                     ss,
                     ss,
                     ss,
                     ss,
                     ss])
    print(len(s))
    print('duration:', time()-t)


def string_concat_test():
    print(timeit.timeit(naive, number=30))
    print(timeit.timeit(faster, number=30))
    n()
    f()


ol = []


def ln():
    nl = []
    for i in ol:
        nl.append(i*2)
    return nl


def lf():
    nl = [i*2 for i in ol]
    return nl


def lf1():
    nl = list(map(lambda x: x*2, ol))
    return nl


def lf2():
    def f(x):
        return x*2
    nl = list(map(f, ol))
    return nl


def lf3():
    nl = (i*2 for i in ol)
    return list(nl)


def loop_test():
    for i in range(100):
        ol.append(i)
    print(timeit.timeit(ln, number=100))
    print(timeit.timeit(lf, number=100))
    print(timeit.timeit(lf1, number=100))
    print(timeit.timeit(lf2, number=100))
    print(timeit.timeit(lf3, number=100))


k = 100


def gf(a, b):
    return a*b


def global_():
    return [gf(100, i) for i in range(1000)]


def local():
    j = 100
    ff = gf
    return [ff(100, i) for i in range(1000)]


def gvl_test():
    # Warm Up
    print(timeit.timeit(global_, number=1000))
    print(timeit.timeit(local, number=1000))
    # Test
    print(timeit.timeit(local, number=1000))
    print(timeit.timeit(global_, number=1000))


def imp0():
    import string
    l = []
    l.append(string.ascii_letters[0])
    return l


import string
def imp1():
    l = []
    l.append(string.ascii_letters[0])
    return l


def import_test():
    print(timeit.timeit(imp0,
                        number=1000))
    print(timeit.timeit(imp1,
                        number=1000))


if __name__ == '__main__':
    # loop_test()
    # gvl_test()
    import_test()
    # import profile
    # profile.run('loop_test()')
