
# yield from iterable = 把这个 iterable 中的元素，一个一个 yield 出去
# yield from 会让父生成器暂时“委托”给子生成器。
1.
def gen():
    yield from [1, 2, 3]
g = gen()

print(next(g))
print(next(g))
print(next(g))
# 1 2 3

2.
def gen1():
    yield from [1, 2, 3]

def gen2():
    for x in [1, 2, 3]:
        yield x
# 写法是一样的

3.
# yield from 后面只能放 Generator，不能放 list?
# 错;yield from放iterable

4.
def child():
    yield 10
    yield 20


def parent():
    yield from child()
    yield 30
    
g = parent()

print(next(g))
print(next(g))
print(next(g))
# 10 20 30

5.
def child():
    print('child start')
    yield 1
    print('child middle')
    yield 2
    print('child end')


def parent():
    print('parent start')
    yield from child()
    print('parent end')
    yield 3
    
g = parent() 
# 生成Generator对象 不执行

print('---1---')
print(next(g))

print('---2---')
print(next(g))

print('---3---')
print(next(g))


# ---1---
# parent start
# child start
# 1
# ---2---
# child middle
# 2
# ---3---
# child end
# parent end
# 3


# parent
#   │
#   │ yield from
#   ↓
# child
#   │
#   ├── yield 1 → 暂停
#   │
#   ├── yield 2 → 暂停
#   │
#   └── 结束
#         ↓
#       回到 parent
#         ↓
#       yield 3
      
# yield from 可以拿到子生成器的 return 值
# 普通yield return 会被塞到Generator 最终结束时，放进 StopIteration 里的返回值

1.
def child():
    yield 10
    yield 20
    return 99


def parent():
    result = yield from child()
    print('result:', result)
    yield 30
    
g = parent()

print(next(g))
print(next(g))
print(next(g))
# 10 20 result： 99 30

2.
# return 99 会把 99 当成一个普通的 yield 值产生出来?
# 不会；会随着异常StopIteration抛出来
# return 99
#    ↓
# 生成器结束
#    ↓
# StopIteration(99)
# return 99 的本质 = 抛出 StopIteration(99)。
# 但在 yield from 中，这个异常被拦截并转换成了赋值（result = 99），
# 所以外部调用者拿到的是 30，而不是 99。99 只在父生成器内部“消化”掉了。


3.
def child():
    yield 1
    return 100


def parent():
    result = yield from child()
100

4.
def child():
    yield 1
    return 100


g = child()

print(next(g))

try:
    print(next(g))
except StopIteration as e:
    print('value =', e.value)
    
# 1 value = 100

# Generator
#    ↓
# yield 1
#    ↓
# next() 得到 1
#    ↓
# 继续执行
#    ↓
# return 100
#    ↓
# Generator 结束
#    ↓
# StopIteration
#    ↓
# StopIteration.value == 100