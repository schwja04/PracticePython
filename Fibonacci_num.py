
fibtable = {1:1, 2:1}

def fib(n):
    global calls
    calls += 1
    if n in fibtable:
        return fibtable[n]
    if n <= 2:
        return 1
    result = fib(n-1) + fib(n-2)
    fibtable[n] = result
    return result

for i in range(1, 110):
    calls = 0
    print(i, fib(i), calls)

import functools

@functools.lru_cache()
def fib2(n):
    if n <= 2:
        return 1
    return fib2(n-1) + fib2(n-2)

for i in range(1, 110):
    calls = 0
    print(i, fib2(i), calls)