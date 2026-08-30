Event Loop（事件循环）
# await、create_task、gather

Event Loop
    ↓
运行 Coroutine
    ↓
遇到 await
    ↓
暂停当前 Coroutine
    ↓
Event Loop 去处理其他事情
    ↓
条件满足
    ↓
恢复 Coroutine

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
    
Coroutine
   ↓
create_task()
   ↓
Task
   ↓
交给 Event Loop 调度


Coroutine
coro = task1()
只是：
Coroutine Object
它本身不会自动运行。

task = asyncio.create_task(task1())
变成：
Task
Task 会被事件循环调度执行。

Coroutine
= “我要执行的异步代码”

Task
= “已经交给 asyncio 安排执行的异步任务”

async def
   ↓
Coroutine Function
   ↓
foo()
   ↓
Coroutine Object
   ↓
┌───────────────┐
│               │
await           create_task()
│               │
↓               ↓
等待执行         Task
│               │
└───────┬───────┘
        ↓
    Event Loop
        ↓
    调度执行
        ↓
 asyncio.gather()
        ↓
    多任务并发
    
    
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
1. create_task() 创建出来的 task1 是 Coroutine 还是 Task？
Task
2. create_task() 之后，work('A', 2) 和 work('B', 1) 会不会开始被调度执行？
会开始被调度
3. print('main继续执行') 会不会等 A、B 执行完才打印？
不会
4. 最终输出顺序是什么？
main继续执行
A 开始
B 开始
B 结束
A 结束
A B

create_task()
    ↓
创建 / 调度 Task

gather()
    ↓
等待多个异步任务
    ↓
统一拿结果

可以这么理解：
create_task
像是：
叫两个人去干活。
create_task(A)
create_task(B)
A → 去干活
B → 去干活
你可以暂时不管他们。

gather
像是：
等这几个人全部干完，然后把结果统一拿回来。
A ──→ 完成 ──┐
              ├──→ gather → [A结果, B结果]
B ──→ 完成 ──┘