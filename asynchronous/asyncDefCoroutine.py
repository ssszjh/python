async def hello():
    return 'hello'
  
result = hello()

print(result)

# 不会得到 'hello'。
# 而是得到一个：
# coroutine object
# <coroutine object hello at 0x...>

# 定义的不是普通函数，而是一个协程函数（coroutine function）

# 普通函数

# hello()
#   ↓
# 立即执行
#   ↓
# return 'hello'

# async def hello()

# hello()
#   ↓
# 创建 Coroutine
#   ↓
# 暂时不执行


import asyncio


async def hello():
    return 'hello'


async def main():
    result = await hello()
    print(result)


asyncio.run(main())

# await 会让出当前协程的执行权，让事件循环有机会去运行其他任务

import asyncio


async def task1():
    print('task1 开始')
    await asyncio.sleep(2)
    print('task1 结束')


async def task2():
    print('task2 开始')
    await asyncio.sleep(1)
    print('task2 结束')
    
# task1 开始
# task2 开始

# 等待 1 秒

# task2 结束

# 再等待 1 秒

# task1 结束

# await asyncio.sleep(2)
# 不是让整个 Python 程序傻等 2 秒。

# 而是：

# task1
#  ↓
# await
#  ↓
# 暂时让出执行权
#  ↓
# 事件循环去执行其他任务


# Generator
#     yield
#       ↓
# 暂停 / 让出控制权


# Coroutine
#     await
#       ↓
# 暂停 / 让出控制权

# asyncio.run()
# 启动一个事件循环，然后运行这个 Coroutine。


import asyncio


async def foo():
    print('A')
    return 100


async def main():
    print('B')

    result = foo()

    print('C')
    print(result)

    value = await foo()

    print('D')
    print(value)


asyncio.run(main())

1.
result = foo()

# 此时 result 是什么？
# A. 100
# B. Coroutine
# C. Generator
# D. Iterator
# B

2.
# 执行到：
# result = foo()
# 会不会立即打印：
# A
# 不会 只是创建 Coroutine Object 不会执行函数体

3.
# value = await foo()
# 执行时，foo() 里的：
# print('A')
# 会执行

4.
# B C Coroutine object a d 100

5.
# result = foo()返回的是Coroutine object 
# await foo()
# 相当于告诉 Python：
# 把这个 Coroutine 交给当前的异步执行机制运行，并等待它完成

# foo()
#  ↓
# Coroutine Object
#  ↓
# await
#  ↓
# 开始/继续执行 Coroutine
#  ↓
# print('A')
#  ↓
# return 100
#  ↓
# 得到 100

# ① async def
#       ↓
# 定义协程函数


# ② foo()
#       ↓
# 创建 Coroutine Object


# ③ await foo()
#       ↓
# 运行/等待这个 Coroutine
