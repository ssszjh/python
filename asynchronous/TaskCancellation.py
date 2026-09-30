# raise
# 我做完清理了，现在继续把取消信号往外传。

# gather(..., return_exceptions=True)
# 等待这些 Task 真正完成取消/清理过程

import asyncio


1.
async def work():
    await asyncio.sleep(10)

task = asyncio.create_task(work())

task.cancel()

print(task.cancelled())

# print 最可能输出什么？
False

2.
async def work():
    try:
        print('A')
        await asyncio.sleep(10)
    except asyncio.CancelledError:
        print('B')
        await asyncio.sleep(2)
        print('C')
        raise


async def main():
    task = asyncio.create_task(work())

    await asyncio.sleep(1)

    task.cancel()

    print('D', task.cancelled())

    await task

    print('E', task.cancelled())

# ① 输出顺序是什么？
# A D False B C E True
# ② D 后面的 task.cancelled() 是 True 还是 False？
False
# ③ E 后面的是什么？
True

3.
# 为什么要 raise
async def work():
    try:
        await asyncio.sleep(10)
    except asyncio.CancelledError:
        print('cleanup')

async def main():
    task = asyncio.create_task(work())

    await asyncio.sleep(1)

    task.cancel()

    await task

    print(task.cancelled())
    print(task.done())

# ① 最后两个输出分别是什么？
# 没有 raise
# False True
# ② 为什么这个 Task 不一定处于 CANCELLED？
# Task 收到了取消请求，但 coroutine 把 CancelledError 捕获并吞掉了，没有重新 raise。因此 Task 最终正常返回，而不是进入 CANCELLED 状态。

4.
async def work():
    try:
        print('start')
        await asyncio.sleep(10)
    except asyncio.CancelledError:
        print('cancel received')

        await asyncio.sleep(3)

        print('cleanup done')
        raise

async def main():
    task = asyncio.create_task(work())

    await asyncio.sleep(1)

    task.cancel()

    print('cancel called')

    await task

    print('task finished')

# 输出顺序是什么？
# start 
# cancel called
# cancel received
# cleanup done

5.
tasks = [
    task_a,
    task_b,
    task_c
]
for task in tasks:
    task.cancel()

async def main():
    await asyncio.gather(
        *tasks,
        return_exceptions=True
    )

print('all cleaned')
# 为什么这里推荐：
# return_exceptions=True
# 而不是：
# return_exceptions=False
# 请从 “取消本身会产生什么结果” 这个角度回答。
# 等待这些 Task 真正完成取消/清理过程

6.
# 假设你的 AI Agent 同时启动：
# RAG     运行 10 秒
# Search  运行 5 秒
# LLM     运行 20 秒
# 用户在第 2 秒点击：
# 停止生成
# 你设计了：
tasks = [
    rag_task,
    search_task,
    llm_task
]

for task in tasks:
    task.cancel()

async def main():
    await asyncio.gather(
        *tasks,
        return_exceptions=True
    )
    
print('Agent stopped')


# 请回答：
# ① task.cancel() 是不是意味着三个任务已经立即结束？
# 不是立即结束，只是通知结束
# ② 为什么还需要 gather()？
# 等待这些 Task 真正完成取消/清理过程
# ③ 如果 LLM 内部有：
try:
    ...
except asyncio.CancelledError:
    close_connection()
    raise

# 这里的 raise 为什么不能随便删？
取消继续信号往外传

# ④ 如果你要给这个 Agent 写一个“优雅停止”的机制，你认为：
# cancel
# → CancelledError
# → cleanup
# → raise
# → gather
# 这条链路分别代表什么？
# cancel() 发起取消请求 → 
# 事件循环向协程抛入 CancelledError → 
# 协程在 cleanup 中做收尾 → 
# raise 重新抛出以继续传播 → 
# 最终由 gather 等聚合层接收并向上传播，完成整个取消流程。

#                  task.cancel()
#                        │
#                        ▼
#               发起取消请求
#                        │
#                        ▼
#               Task 收到 CancelledError
#                        │
#                        ▼
#           ┌─────── try / except ───────┐
#           │                            │
#           ▼                            ▼
#        cleanup                       不处理
#           │                            │
#           ▼                            ▼
#         raise                     CancelledError
#           │                            │
#           ▼                            ▼
#    Task → CANCELLED              Task → CANCELLED
#                                      ↑
#                          （如果没有吞掉异常）

# task.cancel() 并不会立即终止 Task，而是向 Task 发起取消请求。
# Task 在后续执行过程中收到 CancelledError，可以在 except / finally 中执行资源清理。
# 如果希望保留取消语义，通常在清理完成后重新 raise CancelledError，使 Task 最终进入 CANCELLED 状态。
# 调用方通常需要继续 await 这些 Task，例如通过 gather(..., return_exceptions=True)，确保取消和资源清理真正完成。

# 1.try / except / finally 遇到 Cancellation 的执行顺序
# 2.Cancellation 的竞态（Race Condition）
# 3.HTTP / LLM Streaming 中如何优雅取消

async def work():
    try:
        print('A')
        await asyncio.sleep(10)
        print('B')
    except asyncio.CancelledError:
        print('C')
        raise
    finally:
        print('D')


async def main():
    task = asyncio.create_task(work())

    await asyncio.sleep(1)

    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        print('E')

# 最终输出顺序是什么？
# A C D E

2.
async def work():
    try:
        await asyncio.sleep(10)
    finally:
        print('cleanup')


async def main():
    task = asyncio.create_task(work())

    await asyncio.sleep(1)

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print('cancelled')

# 最终会不会执行：cleanup
# 会执行； 不管这个任务最后是成功、失败还是被取消，我都要做这个清理。”

3.
async def work():
    try:
        await asyncio.sleep(10)
    except asyncio.CancelledError:
        print('cancel')
        # 没有 raise
    finally:
        print('cleanup')

async def main():
    task = asyncio.create_task(work())

    await asyncio.sleep(1)

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print('E')

    print(task.done())
    print(task.cancelled())

# ① 输出顺序？  A C D
# ② done() 是什么？ True
# ③ cancelled() 是什么？ False
# | Task 状态 | `done()` | `cancelled()` |
# | ------- | -------: | ------------: |
# | 运行中     |    False |         False |
# | 正常完成    |     True |         False |
# | 异常结束    |     True |         False |
# | 取消结束    |     True |          True |


4.
if task.done():
    result = task.result()
else:
    task.cancel()

# 为什么这段代码不能保证：
# “如果 Task 没完成，我就一定能够成功取消它。”

# 请你结合：
# 检查状态
# ↓
# 状态变化
# ↓
# 执行 cancel()
# 解释一下。
# 因为可能在检查状态的时候，状态就发生变化了，没法cancel；以及去cancel，只是去通知，没法得到一定保证取消成功的通知

5.
async def call_llm():
    client = create_client()

    try:
        ...
    except asyncio.CancelledError:
        ...
        raise
    finally:
        ...

# try 里面放什么？ 这里放的是主要业务逻辑，如：解析LLM Streaming...
# except CancelledError 里面放什么？ 记录日志
# raise 的作用是什么？ 重新抛出 CancelledError，让上层知道这个 Task 是被取消的，并保持 Task 的取消语义
# finally 里面放什么？ 关闭client

# 你重点从 LLM Streaming + 用户点击“停止生成” 的场景来回答。

# 用户点击停止
#       ↓
# task.cancel()
#       ↓
# CancelledError
#       ↓
# ┌─────────────────────────┐
# │ except CancelledError   │
# │ 记录取消 / 业务处理      │
# │ raise                   │
# └─────────────────────────┘
#       ↓
# ┌─────────────────────────┐
# │ finally                 │
# │ 关闭连接 / 释放资源      │
# └─────────────────────────┘
#       ↓
# Task = CANCELLED
#       ↓
# gather(..., return_exceptions=True)
#       ↓
# 所有 Task 完成清理