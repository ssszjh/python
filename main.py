def child():
    yield 10
    return 99
    yield 20
    


def parent():
    result = yield from child()
    print('result:', result)
    yield 30
    
g = parent()

print(next(g))
print(next(g))
print(next(g))