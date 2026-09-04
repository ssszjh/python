# Event Loop（事件循环）
# await、create_task、gather

# Event Loop
#     ↓
# 运行 Coroutine
#     ↓
# 遇到 await
#     ↓
# 暂停当前 Coroutine
#     ↓
# Event Loop 去处理其他事情
#     ↓
# 条件满足
#     ↓
# 恢复 Coroutine

import asyncio


async def task1():
    print('task1 开始')
    await asyncio.sleep(2)
    print('task1 结束')


async def task2():
    print('task2 开始')
    await asyncio.sleep(1)
    print('task2 结束')


async def main():
    await task1()
    await task2()


asyncio.run(main()) 
# 3秒

asyncio.gather(task1(), task2())
# 让多个 Coroutine 一起被事件循环调度，并等待它们全部完成
# 2秒

# Task
async def main():
    task1 = asyncio.create_task(task1())
    task2 = asyncio.create_task(task2())

    await task1
    await task2
    
# Coroutine
#    ↓
# create_task()
#    ↓
# Task
#    ↓
# 交给 Event Loop 调度


# Coroutine
# coro = task1()
# 只是：
# Coroutine Object
# 它本身不会自动运行。

# task = asyncio.create_task(task1())
# 变成：
# Task
# Task 会被事件循环调度执行。

# Coroutine
# = “我要执行的异步代码”

# Task
# = “已经交给 asyncio 安排执行的异步任务”

# async def
#    ↓
# Coroutine Function
#    ↓
# foo()
#    ↓
# Coroutine Object
#    ↓
# ┌───────────────┐
# │               │
# await           create_task()
# │               │
# ↓               ↓
# 等待执行         Task
# │               │
# └───────┬───────┘
#         ↓
#     Event Loop
#         ↓
#     调度执行
#         ↓
#  asyncio.gather()
#         ↓
#     多任务并发
    
    
import asyncio


async def work(name, seconds):
    print(name, '开始')

    await asyncio.sleep(seconds)

    print(name, '结束')

    return name


async def main():
    task1 = asyncio.create_task(work('A', 2))
    task2 = asyncio.create_task(work('B', 1))

    print('main继续执行')

    result1 = await task1
    result2 = await task2

    print(result1, result2)


asyncio.run(main())
# 1. create_task() 创建出来的 task1 是 Coroutine 还是 Task？
# Task
# 2. create_task() 之后，work('A', 2) 和 work('B', 1) 会不会开始被调度执行？
# 会开始被调度;
# 那为什么不是先打印开始呢，而是main继续执行？
# asyncio.create_task 是立即调度（把协程包装成 Task 扔进事件循环的就绪队列），不需要等到 await。
# 但是，任务体内的代码实际执行，确实要等到 main 函数遇到第一个 await 交出控制权后，事件循环才会去运行这些任务。
# task1 = create_task(work('A', 2))：此时 work('A') 被立即调度（放入队列），但并未执行（因为 main 协程还在拿着 CPU 往下走）。
# task2 = create_task(work('B', 1))：同理，work('B') 被立即调度，并未执行。
# print('main继续执行')：立即打印。
# result1 = await task1：到了这里，main 协程挂起，将控制权交还给事件循环。事件循环这才开始从队列里取任务执行。
# create_task 只管“报名参赛”（立即调度），await 才是“发令枪响”（触发事件循环去跑比赛）


3. 
# print('main继续执行') 会不会等 A、B 执行完才打印？
# 不会
4. 
# 最终输出顺序是什么？
# main继续执行
# A 开始
# B 开始
# B 结束
# A 结束
# A B

# create_task()
#     ↓
# 创建 / 调度 Task

# gather()
#     ↓
# 等待多个异步任务
#     ↓
# 统一拿结果

# 可以这么理解：
# create_task
# 像是：
# 叫两个人去干活。
# create_task(A)
# create_task(B)
# A → 去干活
# B → 去干活
# 你可以暂时不管他们。

# gather
# 像是：
# 等这几个人全部干完，然后把结果统一拿回来。
# A ──→ 完成 ──┐
#               ├──→ gather → [A结果, B结果]
# B ──→ 完成 ──┘

import asyncio


async def a():
    print('A开始')
    await asyncio.sleep(2)
    print('A结束')
    return 'A'


async def b():
    print('B开始')
    await asyncio.sleep(1)
    print('B结束')
    return 'B'


async def main():

    task_a = asyncio.create_task(a())

    print('main 1')

    result_b = await b()

    print('main 2')

    result_a = await task_a

    print('main 3')

    print(result_a, result_b)


asyncio.run(main())


# ① 最终大概需要几秒？ 
# 2
# ② 输出顺序是什么？
# main 1  B开始 A开始 B结束 main 2 A结束 main 3 A,B
# create_task 立即调度，但不立即执行：A开始 打印在 main 1 之后，而不是之前，因为 main 函数直到 await b() 才交出控制权。
# await 的“趁虚而入”：虽然你写的是 await b()，但在 b 睡眠期间，事件循环会自动去执行已经调度的 task_a，这展示了 asyncio 的协作式并发特性。
# 先执行完 b 再 await task_a：main 2 打印在 A结束 之前，说明代码是顺序执行的——先等 b() 彻底完成，才去等 task_a。虽然 a 和 b 在并发运行，但代码流程严格遵循 await 的顺序。

# 为什么是B开始 A开始而不是A开始 B开始呢？
# 因为 await b() 会立即进入 b() 函数内部，并一口气执行完 print('B开始') 之后，才遇到 await asyncio.sleep(1) 交出控制权。
# 第 0 步（创建任务）：create_task(a()) 确实执行了，但这只是把 a() 的“名片”贴到了事件循环的等待队列里。此时 a() 函数内部的代码连一个字节都没执行，print('A开始') 还静静地躺在函数里。
# 第 1 步（遇到 await b()）：main 执行到这一行。注意，await b() 并不是“把 b 放到队列等”，而是直接调用函数 b()。
# 第 2 步（B 抢跑成功）：程序进入 b() 函数，顺序执行。由于 print('B开始') 是同步代码（没有 await），它会立即执行。所以这时候 B开始 被打印出来。
# 第 3 步（B 让出控制权）：接着执行到 await asyncio.sleep(1)，b() 发现要等 1 秒，于是它告诉事件循环：“我先睡会儿”。直到这一刻，main 才把 CPU 控制权交还给事件循环。
# 第 4 步（事件循环翻牌）：事件循环拿到控制权后，发现队列里躺着之前创建的 task_a，于是才去执行 a()，此时 A开始 才被打印。

# ③ 为什么 a() 和 b() 会同时进行？
# create_task是当前 Event Loop 中创建一个 Task
# ④ 如果把：
# task_a = asyncio.create_task(a())
# 改成：
# result_a = await a()
# 那么总耗时会变成多少？
# 3

# ⑤ 最后一个问题：
# 为什么这里使用 create_task(a()) 是有意义的，而直接：
# await a()
# 就失去了它的意义？
# create_task() 的价值是：让任务提前开始执行，我可以先去做别的事情。


import asyncio
import time


async def a():
    print('A开始')
    await asyncio.sleep(2)
    print('A结束')


async def b():
    print('B开始')
    await asyncio.sleep(1)
    print('B结束')


async def main():
    task_a = asyncio.create_task(a())
    task_b = asyncio.create_task(b())

    await task_a
    await task_b


asyncio.run(main())

1.
# A 和 B 是否会并发执行？
# 并发执行，是两个不同的task
2.
# 最终输出顺序是什么？
# A开始 B开始 B结束 A结束
3.
# 总耗时大约是 1 秒、2 秒还是 3 秒？
2
4.
# 把：await asyncio.sleep(2)换成：time.sleep(2)会发生什么？
# 是整个线程阻塞了2秒，其他task无法并行进行；总耗时为3

# while True:

#     找到可以运行的 Task

#     让它运行一小段

#     如果 Task 遇到 await：
#         暂停它

#     看看有没有其他 Task 可以运行

#     重复
    
# async def
#    ↓
# Coroutine Function

# foo()
#    ↓
# Coroutine Object

# create_task(foo())
#    ↓
# Task
#    ↓
# 交给 Event Loop

# Task 开始执行
#    ↓
# 遇到 await
#    ↓
# 当前 Task 暂停
#    ↓
# 控制权回到 Event Loop
#    ↓
# Event Loop 找其他可以运行的 Task
#    ↓
# 其他 Task 执行
#    ↓
# 等待条件满足
#    ↓
# 原 Task 恢复