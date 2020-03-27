import math

def func_a(x, k):
    a = 1
    yield a
    for i in range(1, k + 1):
        a *= x**2 / (2*i * (2*i - 1))
        yield a

def func_b(n):
    p = 2
    yield p
    for i in range(2, n + 1):
        p *= 1 + 1 / i**2
        yield p

def func_c(a, b, n):
    d2 = a + b
    d1 = a**2 + a*b + b**2
    yield d2
    if n > 1:
        yield d1
    for i in range(3, n + 1):
        d1, d2 = (a + b) * d1 - a * b * d2, d1
        yield d1

def func_d(n):
    sum = 0
    a3 = 1
    a2 = 1
    a1 = 1
    i = 1
    while i <= n and i <= 3:
        sum += 1 / 2**i
        yield sum
        i += 1
    for i in range(4, n + 1):
        a1, a2, a3 = a1 + a3, a1, a2
        sum += a1 / 2**i
        yield sum

def func_e(x, e):
    e *= 1 - x**2
    a = 2 * x
    res = a
    yield res
    i = 1
    while a > e:
        i += 2
        a *= x**2
        res += a / i
        yield res

#####################################################################################################################################
print("A"*20)
i = 0
x = 2
n = 10
for k in func_a(x, n):
    print("X{} = {}".format(i, k))
    i += 1
print()

print("B"*20)
i = 1
n = 10
for k in func_b(n):
    print("P{} = {}".format(i, k))
    i += 1
print()

print("C"*20)
i = 1
a = 2
b = 3
n = 10
for k in func_c(a, b, n):
    print("DET{} = {}".format(i, k))
    i += 1
print()

print("D"*20)
i = 1
n = 10
for k in func_d(n):
    print("S{} = {}".format(i, k))
    i += 1
print()

print("E"*20)
i = 1
x = 0.95
e = 0.00000000001
for k in func_e(x, e):
    print("ln_app_{} = {}".format(i, k), "Error = {}".format(abs(k - math.log((1 + x) / (1 - x), math.e))), sep = "\t")
    i += 1
print()