# 异步异常处理

# work()
#   ↓
# 执行
#   ↓
# raise ValueError
#   ↓
# 异常沿着 coroutine 返回
#   ↓
# await work()
#   ↓
# try / except 捕获

# Task
#  │
#  │ work() 出异常
#  ↓
# Task 保存异常
#  │
#  │ await task
#  ↓
# 异常重新抛出
#  │
#  ↓
# try / except 捕获


import asyncio

async def work():
    print('开始')
    await asyncio.sleep(1)
    raise ValueError('出错了')

async def main():
    task = asyncio.create_task(work())

    try:
        result = await task
        print('结果:', result)
    except ValueError as e:
        print('捕获:', e)

asyncio.run(main())

1. 
# 会不会打印：开始
# 会打印开始
2. 
# 会不会打印：结果: ...
# 不会打印结果：...
3. 
# 最终会不会进入 except？
# 会进入except
4. 
# 最终输出的完整顺序是什么？
# 开始 捕获: 出错了

# Task 的 cancel()
# task.cancel()  请求这个 Task 停止执行
# 给 Task 发一个取消请求。
import asyncio

async def work():
    print('A')

    try:
        await asyncio.sleep(10)
        print('B')
    except asyncio.CancelledError:
        print('C')

async def main():
    task = asyncio.create_task(work())

    await asyncio.sleep(1)

    task.cancel()

    print('D')

    await task

    print('E')

asyncio.run(main())

1. 
# A 会不会打印？
# 会
2. 
# B 会不会打印？
# 不会
3. 
# C 会不会打印？
# 会
4. 
# D 会不会打印？
# 会
5. 
# E 会不会打印？
# 会
6. 
# 最终输出顺序是什么？
# A D C E

import asyncio

async def work():
    print('A')
    await asyncio.sleep(10)
    print('B')

async def main():
    task = asyncio.create_task(work())

    await asyncio.sleep(1)

    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        print('C')

    print('D')

asyncio.run(main())

# 1. 
# A 会打印吗？
# 会

# 2. 
# B 会打印吗？
# 不会
# 3. 
# await task 会不会触发 CancelledError？
# 会触发
# 4. 
# C 会打印吗？
# 会
# 5. 
# 最终输出顺序是什么？
# A C D

# gather() 的异常和取消
import asyncio

async def work_a():
    print('A开始')
    await asyncio.sleep(1)
    raise ValueError('A出错了')

async def work_b():
    print('B开始')
    await asyncio.sleep(2)
    print('B结束')
    return 'B结果'

async def main():
    try:
        results = await asyncio.gather(
            work_a(),
            work_b()
        )
        print(results)
    except ValueError as e:
        print('捕获:', e)

asyncio.run(main())

# 1. 
# A开始 会打印吗？
# 会
# 2. 
# B开始 会打印吗？
# 会
# 3. 
# A出错了 后，B结束 会不会打印？
# 不会
# 4. 
# 会不会进入 except？
# 会
# 5. 
# 最终输出顺序是什么？
# A开始 B开始  捕获:A出错了

# gather 默认行为（return_exceptions=False）是立即将异常传播，并取消所有未完成的任务。

# TaskGroup
# 把一组 Task 放进一个“任务组”里统一管理。

async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(work('A', 2))
        tg.create_task(work('B', 1))
        tg.create_task(work('C', 3))

    print('全部完成')
# 只有 TaskGroup 里面的所有任务都结束之后，才会离开 async with。
# create_task()
#     ↓
# 创建一个 Task

# TaskGroup
#     ↓
# 管理一组 Task

import asyncio

async def work(name, delay):
    print(f'{name} 开始')
    await asyncio.sleep(delay)
    print(f'{name} 结束')

async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(work('A', 2))
        tg.create_task(work('B', 1))

    print('TaskGroup结束')
    print('main结束')

asyncio.run(main())

# 第 1 题
# 下面哪些输出一定会出现？
# A.A 开始
# B.B 开始
# C.B 结束
# D.A 结束
# E.TaskGroup结束
# F.main结束
# A B C D E F

# 第 2 题
# 下面两个输出：
# A 结束
# TaskGroup结束
# 谁一定先出现？
# A 结束

# 第 3 题
# 如果把：
# async with asyncio.TaskGroup() as tg:
#     tg.create_task(work('A', 2))
#     tg.create_task(work('B', 1))

# print('TaskGroup结束')
# 理解成：
# “创建完 A、B 后，马上执行 TaskGroup结束”
# 这个理解对不对？为什么？
# 错；是创建并执行完成A、B 后，马上执行 TaskGroup结束

# TaskGroup 不只是负责创建任务，更重要的是负责等待和管理这一组任务。
# 进入 TaskGroup
#     ↓
# 创建 A Task
# 创建 B Task
#     ↓
# A、B 并发执行
#     ↓
# 等待 A、B 都完成
#     ↓
# 离开 async with
#     ↓
# TaskGroup结束