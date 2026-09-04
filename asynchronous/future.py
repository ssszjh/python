# Future
# Future = 一个“未来会产生结果”的占位对象。

# Task A
#   ↓
# “我要等网络请求结果”
# Task A
#   ↓
# Future
#   ↓
# 等待网络结果

# Future

# ┌──────────────┐
# │   PENDING    │  ← 正在等待
# └──────┬───────┘
#        │
#        ↓
# ┌──────────────┐
# │  FINISHED    │  ← 已经完成
# └──────────────┘

# Coroutine
# async def get_data():
#     return 100

# 调用：
# coro = get_data()

# 得到：
# Coroutine

# 它代表：
# 一段可以被执行的异步代码。

# Coroutine
# = “我要做什么”

# Future
# = “最终会得到什么”

# Task = 被 Event Loop 调度执行的 Coroutine，并且它本身也是一个 Future-like 的对象。
# Coroutine
#     ↓
# create_task()
#     ↓
# Task
#     ↓
# 被 Event Loop 调度
#     ↓
# 最终产生 result

# 普通业务开发
#    ↓
# async / await
# Task
# gather
#    ↓
# 已经够用了

# 底层 asyncio
#    ↓
# Future
# Event Loop
# Callbacks
#    ↓
# 才经常出现

#                  Event Loop
#                      │
#                      ↓
#                   Task
#                      │
#                      ↓
#                 执行 Coroutine
#                      │
#                      ↓
#               Future-like result
#                      │
#                      ↓
#                   完成
#                      │
#                      ↓
#                 await task
#                      │
#                      ↓
#                   得到结果
                  
                  
# Coroutine
#    ↓
# “代码”

# Task
#    ↓
# “正在被调度执行的代码”

# Future
#    ↓
# “未来的结果”

import asyncio


async def work():
    print('开始')
    await asyncio.sleep(1)
    print('结束')
    return 100


async def main():
    task = asyncio.create_task(work())

    print(task.done())

    result = await task

    print(task.done())
    print(result)


asyncio.run(main())

1.
# 第一次：
# print(task.done())
# 输出：
# True
# 还是：
# False
# False

2.
# 为什么？
# 此时task尚未执行，只是挂起了
# Task 已经被创建并安排执行，但还没有真正开始执行 work()

3.
# 执行：
# result = await task
# 之后，task 是完成状态还是未完成状态？
# 完成

4.
# 第二个：
# print(task.done())
# 输出什么？
# True

5.
# 最终 result 是多少？
# 100

# Coroutine
#    │
#    │ create_task()
#    ↓
# Task
#    │
#    │ Event Loop 调度
#    ↓
# 执行 coroutine
#    │
#    │ return 100
#    ↓
# Task 完成
#    │
#    │ await task
#    ↓
# 得到 100