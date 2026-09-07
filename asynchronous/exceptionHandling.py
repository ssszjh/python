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

# gather() 遇到异常时，不会自动取消其他任务；
# 但如果外层 main() 随后结束，asyncio.run() 清理事件循环时，剩余任务也可能被取消，
# 因此你实际看不到它们继续执行。


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

# TaskGroup：一个子任务发生异常 → 取消其他尚未完成的子任务。
#              TaskGroup
#           ┌──────┼──────┐
#           ↓      ↓      ↓
#           A      B      C
#                  ❌
#                  ↓
#           ┌──────┴──────┐
#           ↓             ↓
#         cancel         cancel
#           ↓             ↓
#           A             C
# 这就是 TaskGroup 的**结构化并发（Structured Concurrency）**思想：
# 一组任务作为一个整体管理，一个任务失败，整个任务组进入失败状态。

# TaskGroup异常
1.
async def main():
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(work_a())
            tg.create_task(work_b())

    except ValueError:
        print('捕获 ValueError')
# 如果 work_a() 抛出：
# ValueError('A出错了')
# 那么：
# A. B 会继续执行到结束
# B. B 会被 TaskGroup 取消
# C. TaskGroup 会忽略 A 的异常
# D. main() 永远不会结束
# B

# 第 2 题
# 下面这个概念你认为是什么意思？
# ExceptionGroup
# A. 把多个异常组合到一起的异常对象
# B. 一个专门创建 Task 的对象
# C. TaskGroup 的别名
# D. Event Loop 的异常
# A

# except vs except*
# except
#   ↓
# 处理一个普通异常

# except*
#   ↓
# 从 ExceptionGroup 中
# 挑出符合类型的异常处理

3.
# 假设一个 ExceptionGroup 里面有：
# ValueError
# TypeError
# RuntimeError
# 代码：
try:
    ...
except* ValueError:
    print('处理 ValueError')
except* TypeError:
    print('处理 TypeError')

# 那么最终：
# A. 三个异常都会被处理
# B. 只有 ValueError 和 TypeError 被处理，RuntimeError 继续向外传播
# C. 只有 ValueError 被处理
# D. except* 不能处理 ExceptionGroup
# B

4.
async def task_a():
    await asyncio.sleep(1)
    raise ValueError('A出错')

async def task_b():
    await asyncio.sleep(1)
    raise TypeError('B出错')

async def task_c():
    await asyncio.sleep(3)
    print('C结束')

async def main():
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(task_a())
            tg.create_task(task_b())
            tg.create_task(task_c())

    except* ValueError:
        print('处理 ValueError')

    except* TypeError:
        print('处理 TypeError')

    print('main结束')

# 最终输出中，下面哪些一定会出现？
# A. 处理 ValueError
# B. 处理 TypeError
# C. C结束
# D. main结束
# 你可以多选。
# 另外想一下：
# C 为什么不会打印？
# A B D；A,B异常时，c被取消了

# TaskGroup
#    │
#    ├── A → 异常
#    ├── B → 异常
#    └── C → 未完成
#             ↓
#       C 被取消
#             ↓
#    ┌────────┴────────┐
#    ↓                 ↓
# ExceptionGroup     Canceled
#    ↓
# except* 分别处理

# TaskGroup返回值
# create_task()
#      ↓
#    Task
#      ↓
# 任务执行
#      ↓
# task.result()
#      ↓
# 拿到返回值

5.
async def work(name):
    await asyncio.sleep(1)
    return f'{name}结果'

async def main():
    async with asyncio.TaskGroup() as tg:
        task_a = tg.create_task(work('A'))
        task_b = tg.create_task(work('B'))

    print(task_a.result())
    print(task_b.result())

# 最终输出是什么？
# A.
# A结果
# B结果
# B.
# [ A结果, B结果 ]
# C.
# None
# None
# D. 报错
# A

# TaskGroup 的取消机制
# 如果外部取消 main()：
# main 被取消
#    ↓
# TaskGroup
#    ↓
# A、B、C
#    ↓
# 全部取消

# 这就是 TaskGroup 的另一个核心特性：
# TaskGroup 中的任务生命周期和父任务绑定。

# 父任务
#   │
#   └── TaskGroup
#        ├── A
#        ├── B
#        └── C

# 父任务取消
#      ↓
# TaskGroup取消
#      ↓
# A、B、C取消

6.
async def work(name):
    try:
        print(f'{name}开始')
        await asyncio.sleep(10)
        print(f'{name}结束')
    except asyncio.CancelledError:
        print(f'{name}被取消')
        raise

async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(work('A'))
        tg.create_task(work('B'))
        tg.create_task(work('C'))

        await asyncio.sleep(1)

        raise asyncio.CancelledError

# 1 秒后 main() 主动抛出 CancelledError。
# 你认为 A、B、C 会怎么样？
# A. 都继续执行
# B. 都被取消
# C. 只有 A 被取消
# D. 只有抛出异常的 main 被取消，A/B/C继续
# B

# TaskGroup
# │
# ├── ① 创建任务
# │      tg.create_task()
# │
# ├── ② 等待任务
# │      async with 结束前等待
# │
# └── ③ 管理任务生命周期
#        ├── 子任务异常 → 取消其他子任务
#        └── 父任务取消 → 取消子任务

7.
async def work_a():
    print('A开始')
    await asyncio.sleep(1)
    raise ValueError('A出错')

async def work_b():
    try:
        print('B开始')
        await asyncio.sleep(3)
        print('B结束')
    except asyncio.CancelledError:
        print('B被取消')
        raise

async def main():
    try:
        async with asyncio.TaskGroup() as tg:
            task_a = tg.create_task(work_a())
            task_b = tg.create_task(work_b())

    except* ValueError:
        print('捕获ValueError')

    print('main结束')

# 最终输出顺序是什么？
# A开始 B开始 B被取消 捕获ValueError main结束

# TaskGroup
# │
# ├── tg.create_task()
# │
# ├── 等待所有子任务结束
# │
# ├── 子任务异常
# │     ↓
# │   取消其他未完成任务
# │     ↓
# │   ExceptionGroup
# │     ↓
# │   except*
# │
# ├── 父任务取消
# │     ↓
# │   子任务一起取消
# │
# └── 任务结果
#       ↓
#     task.result()

# gather() 更偏向“并发执行 + 收集结果”，TaskGroup 更偏向“把一组任务作为一个整体进行生命周期管理”