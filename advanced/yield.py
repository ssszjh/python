# yield / 生成器 / 迭代器 / next()

# return
# vs
# yield

# 生成器是什么
# 为什么 yield 不会一次性把所有数据放内存
# next()
# 迭代器
# for 到底是怎么遍历生成器的

# 调用一个包含 yield 的函数时，函数体不会立即执行，而是先得到一个生成器对象

# 调用 get_numbers()
#         ↓
# 得到 generator
#         ↓
# next(g)
#         ↓
# 开始执行函数
#         ↓
# print('开始执行')
#         ↓
# yield 1
#         ↓
# 暂停
#         ↓
# 返回 1

# yield = “把一个值交出去，然后把函数暂停在这里，下次再继续。”

# 生成器有一个非常重要的特性：
# 惰性计算（lazy evaluation）
# 也就是：
# 用到的时候才计算。

# 假设我要生成：
1
2
3
...
100000000
# 普通写法
def get_numbers():
    result = []

    for i in range(1, 100000001):
        result.append(i)

    return result
# 先生成 1 亿个数字
#         ↓
# 放进 list
#         ↓
# 占用大量内存
#         ↓
# 最后一次性返回

# 生成器
def get_numbers():
    for i in range(1, 100000001):
        yield i
# 它不会一次生成 1 亿个数字
# 需要 1
#  ↓
# 生成 1

# 需要 2
#  ↓
# 生成 2

# 需要 3
#  ↓
# 生成 3
# ...

# 普通函数

# 调用
#  ↓
# 执行
#  ↓
# return
#  ↓
# 结束

# 生成器函数

# 调用
#  ↓
# 得到 generator
#  ↓
# next()
#  ↓
# 执行
#  ↓
# yield
#  ↓
# 暂停
#  ↓
# next()
#  ↓
# 继续执行
#  ↓
# yield
#  ↓
# 暂停
#  ↓
# ...

1.
def test():
    print('A')
    yield 1
    print('B')
    yield 2

g = test()

print('C')
# C

2.
print(next(g))
# A 1

3.
print(next(g))
# B 2

4.
# 为什么不会立即打印 A？
g = test()
# 先返回一个 generator

5.
# 你自己的话解释：
# yield 和 return 最大的区别是什么？
# 1.普通函数调用后遇到return就结束了
# 2.调用“包含 yield 的函数”时，直接得到 generator 对象；真正执行到 yield 是发生在 next() 时
# 3.yield后续调用next 才会执行到最近一个yield中断
# 生成器函数调用时返回 generator，next() 才驱动函数执行，执行到 yield 时暂停，并把 yield 后面的值返回给 next()。


def test():
    yield 10
    yield 20
    yield 30

g = test()

a = next(g)
b = next(g)
c = next(g)

print(a)
print(b)
print(c)
# 10 20 30

def test():
    yield 10
    yield 20

g = test()

print(next(g))
print(next(g))
print(next(g))
# 10 20 StopIteration 生成器已经没有东西可以继续产生了

1.
def test():
    yield 1
    yield 2

g = test()

for x in g:
    print(x)
# 1 2

2.
# 为什么 for 遍历生成器时，不需要我们自己写 next()？
# for 底层就在不断做类似 next() 的事情。
# for
#  ↓
# 获取迭代器
#  ↓
# 不断 next()
#  ↓
# 遇到 StopIteration
#  ↓
# 自动结束循环

3.
def test():
    yield 1
    yield 2

g = test()

print(next(g))
print(next(g))
print(next(g))
# 1 2 StopIteration 生成器已经没有东西可以继续产生了

4.
# 生成器没有更多数据时，会返回 None？
# 错 抛出 StopIteration 异常

# 生成器本身就是一种迭代器。
# Iterable（可迭代对象）
#         ↓
# Iterator（迭代器）
#         ↓
# Generator（生成器）

1.
# g是什么？
g = iter([10, 20, 30])
# A. list
# B. generator
# C. iterator
# D. function
# C

2.
print(next(g))
print(next(g))
print(next(g))
# 10 20 30

3.
next(g)
# StopIteration异常报错

4.
# iter() 和 next() 分别负责什么？
# iter()：从一个可迭代对象中获取它的迭代器。
# next()：让迭代器向前走一步，并获取下一个元素。

# list / tuple / string / dict ...
#         ↓
#    可迭代对象 Iterable
#         ↓
#       iter()
#         ↓
#      Iterator
#         ↓
#       next()
#         ↓
#    一个一个取值

# Generator 是:
# 生成器函数
#    ↓
# yield
#    ↓
# Generator
#    ↓
# 本身就是 Iterator
#    ↓
# 可以 next()
# Generator 是 Iterator 的一种。

1.
numbers = [1, 2, 3]
g = iter(numbers)
# numbers是list;也为可迭代对象 Iterable
# g为Iterator

2.
def test():
    yield 1
    yield 2

g = test()

g 
# 是：D
# A. Iterable
# B. Iterator
# C. Generator
# D. 以上都可以

3.
for x in [1, 2, 3]:
    print(x)

def test():
    yield 1
    yield 2
    yield 3

for x in test():
    print(x)
# 这两个 for 都能工作？
# 第一个for: for的是一个list; list为可迭代对象 Iterable;
# for相当于获取迭代器 不断去next() 所以可以工作
# 第二个for:相当于获取迭代器 不断去next() 所以可以工作

4.
# Iterable（可迭代对象）、Iterator（迭代器）、Generator（生成器）三者到底是什么关系？
# Iterable 是list / tuple / string / dict...
# iterator 是可迭代对象 Iterable iter化后
# Generator 是调用一个包含 yield 的函数时，函数体不会立即执行，而是先得到一个Generator
# 它们之间的关系是 Iterable可以生成iterator 和Generator ;Generator 是 Iterator 的一种
#               Iterable
#               /      \
#              /        \
#        list/tuple/...   Generator
#              ↓             ↓
#           iter()        本身就是
#              ↓             ↓
#           Iterator ←───────┘
          
# Iterable：
# 只要能够通过 iter(obj) 获取 Iterator，就属于可迭代对象。
# Iterator：
# 能够通过 next() 一个一个产生数据，并且自身也可以被 iter()。
# Generator：
# Python 提供的一种特殊 Iterator，通常通过 yield 创建。
# Iterator 是“能不能被遍历”，Iterator 是“负责一个一个取数据”，Generator 是“用 yield 实现的一种 Iterator”。

1.
A = [1, 2, 3]
B = iter(A)
next(A)   
# → ? 报错
next(B)  
#  → ? 1

2.
for x in [1, 2, 3]:
    print(x)
    
numbers = [1, 2, 3]
next(numbers)
# for相当于获取迭代器 不断去next() 所以可以工作

3.
# 所有 Iterable 都是 Iterator。
# 不是;Iterable要可iter()

#                  Iterable
#                     │
#              iter(obj)
#                     ↓
#                 Iterator
#                     │
#                   next()
#                     ↓
#                一个个数据
#                     │
#           没有更多数据
#                     ↓
#              StopIteration
             
# yield
#  ↓
# Generator
#  ↓
# 本身就是 Iterator
#  ↓
# 可以 next()
#  ↓
# 也可以 for

# List Comprehension（列表推导式）
# Generator Expression（生成器表达式）
numbers = [x for x in range(1000000)]
numbers = (x for x in range(1000000))

1.
a = [x for x in range(1000000)]
b = (x for x in range(1000000))
# a 是什么？ 
# a是list Iterable
# b 是什么？ 
# b是Generator

2.
# 下面哪个会一次性把 0～999999 都生成出来并保存起来？ A
A = [x for x in range(1000000)]

B = (x for x in range(1000000))

3.
b = (x for x in range(3))
print(next(b))
print(next(b))
print(next(b))
# 0 1 2
print(next(b))
# 异常

1.
def test():
    yield 1
    yield 2
    yield 3

g = test()

for x in g:
    print(x)

print('第二次')

for x in g:
    print(x)
    
# 1 2 3 第二次 
# 因为 for 会自动处理：
# StopIteration

2.
# 为什么第二个 for 什么都没有？
# 因为已经yield完了

3.
a = [1, 2, 3]
b = iter(a)
# 谁保存数据？谁负责一个一个取数据？
# a保存数据;b负责一个一个取数据

4.
# 为什么 Generator 可以节省内存？
# 因为他是调一次next才取一次数据

# yield
#  ↓
# Generator
#  ↓
# Iterator
#  ↓
# next()
#  ↓
# 一个一个产生数据
#  ↓
# StopIteration


# Iterable
#  ↓
# iter()
#  ↓
# Iterator
#  ↓
# next()

# for
#  ↓
# iter()
#  ↓
# 不断 next()
#  ↓
# StopIteration
#  ↓
# 自动结束

# Generator
#  ↓
# 惰性计算
#  ↓
# 按需产生数据
#  ↓
# 节省内存

