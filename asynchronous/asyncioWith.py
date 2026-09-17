# asyncio.wait
# 等待一组 Task，并把它们分成「已经完成」和「还没完成」两组。

# FIRST_COMPLETED / FIRST_EXCEPTION / ALL_COMPLETED
# return_when=
# asyncio.ALL_COMPLETED
# asyncio.FIRST_COMPLETED
# asyncio.FIRST_EXCEPTION

# ALL_COMPLETED 默认
# 所有任务完成以后才返回。

# FIRST_COMPLETED
# 只要有一个任务完成，wait() 就立即返回。
# FIRST_COMPLETED
#         ↓
# 一个完成
#         ↓
# wait 返回
#         ↓
# done   → 已完成任务
# pending → 仍然运行中的任务

# 而：wait()不会因为返回了就自动取消 pending。

# FIRST_EXCEPTION
# 只要有一个 Task 抛出异常，就返回
# IRST_EXCEPTION：
# 不会自动取消 pending。
# 所以：
# B 出错
#  ↓
# wait 返回
#  ↓
# A、C 仍然可能继续运行
# 这和TaskGroup 有一个非常重要的区别。

# TaskGroup
# → 失败传播 + 自动取消兄弟任务

# wait(FIRST_EXCEPTION)
# → 发现异常就返回，但不负责取消 pending

# | 模式                | 什么时候 `wait()` 返回 | pending 自动取消？ |
# | ----------------- | ---------------- | ------------- |
# | `ALL_COMPLETED`   | 全部完成             | ❌             |
# | `FIRST_COMPLETED` | 任意一个完成           | ❌             |
# | `FIRST_EXCEPTION` | 任意一个抛异常          | ❌             |

# done返回的是一个任务，不是result
# done, pending = await asyncio.wait(tasks)
# done === task

# 拿结果需要
# for task in done:
#     result = task.result()

import asyncio

async def work(name, delay, error=False):
    print(f'{name} 开始')

    await asyncio.sleep(delay)

    if error:
        print(f'{name} 出错')
        raise ValueError(f'{name} error')

    print(f'{name} 结束')
    return name


async def main():
    a = asyncio.create_task(work('A', 3))
    b = asyncio.create_task(work('B', 1, True))
    c = asyncio.create_task(work('C', 5))

    done, pending = await asyncio.wait(
        [a, b, c],
        return_when=asyncio.FIRST_EXCEPTION
    )

    print('wait 返回')

    for task in done:
        try:
            print('结果:', task.result())
        except Exception as e:
            print('异常:', type(e).__name__)

    print('pending 数量:', len(pending))

    await asyncio.sleep(6)

    print('main 结束')


asyncio.run(main())

# 1. 
# A / B / C 会不会全部开始？
# 会

# 2. 
# 大概输出顺序是什么？重点写出前面的顺序即可。
# A开始
# B开始
# C开始
# B出错
# wait 返回
# 异常: ValueError
# pending 数量: 2
# A结束
# C结束
# main 结束

# 3. 
# B 在 1 秒后抛出异常时，wait() 会不会立即返回？
# 会

# 4. 
# wait 返回 执行时：
# done 里面是谁？
# pending 里面是谁？
# done 里面是b
# pending 里面是a、c

# 5. 
# pending 里面的 A、C 会不会因为 wait() 返回而自动取消？
# 不会

# 6. 
# 最后 main 结束 之前，A 和 C 会不会继续执行？
# 会

#                 asyncio.wait()
#                      │
#           ┌──────────┼──────────┐
#           ↓          ↓          ↓
#    ALL_COMPLETED  FIRST_COMPLETED  FIRST_EXCEPTION
#        │               │              │
#    全部结束         一个结束         一个异常
#        │               │              │
#        └───────────────┴──────────────┘
#                        ↓
#                  返回 done/pending
#                        ↓
#                ❌ 不自动取消 pending

# TaskGroup
# 一个任务异常
#      ↓
# 取消其他兄弟任务
#      ↓
# ExceptionGroup

# timeout
# 时间到了就返回 注意是返回，不是取消，不会取消原任务

# cancel()
# 取消任务
# for task in pending:
#     task.cancel()

# await asyncio.gather(
#     *pending,
#     return_exceptions=True
# )

# cancel()
#    ↓
# 通知任务：准备取消

# gather()
#    ↓
# 等待任务：你们都收尾结束

# asyncio.wait()
#         │
#         ├── ALL_COMPLETED
#         │       └── 全部完成才返回
#         │
#         ├── FIRST_COMPLETED
#         │       └── 一个完成就返回
#         │
#         ├── FIRST_EXCEPTION
#         │       └── 一个异常就返回
#         │
#         └── timeout
#                 └── 时间到了也返回

import asyncio


async def work(name, delay):
    print(f'{name} 开始')

    try:
        await asyncio.sleep(delay)
        print(f'{name} 完成')
        return name

    except asyncio.CancelledError:
        print(f'{name} 被取消')
        raise


async def main():
    a = asyncio.create_task(work('A', 5))
    b = asyncio.create_task(work('B', 2))
    c = asyncio.create_task(work('C', 4))

    done, pending = await asyncio.wait(
        [a, b, c],
        timeout=3,
        return_when=asyncio.FIRST_COMPLETED
    )

    print('wait 返回')

    for task in done:
        print('结果:', task.result())

    print('pending 数量:', len(pending))

    for task in pending:
        task.cancel()

    await asyncio.gather(
        *pending,
        return_exceptions=True
    )

    print('main 结束')


asyncio.run(main())

# 1. 
# A、B、C 会不会全部开始？
# 会

# 2. 
# wait() 是因为 timeout=3 返回，
# 还是因为 FIRST_COMPLETED 返回？
# FIRST_COMPLETED；因为b是2秒

# 3. 
# wait 返回时：
# done 里面是谁？
# pending 里面是谁？
# done 里面是b
# pending 里面是a和c

# 4. 
# 大概的输出顺序是什么？
# A 开始
# B开始
# C 开始
# B完成
# wait 返回
# 结果:B
# pending 数量: 2
# A 取消
# C 取消
# main 结束

# 5. 
# A 和 C 被 cancel() 后，
# except asyncio.CancelledError 会不会执行？
# 会

# 6. 
# 为什么 cancel() 后还需要：
# await asyncio.gather(*pending, return_exceptions=True)
# 通知全部任务收尾

# asyncio.shield()
# 外层取消
#    ↓
# shield
#    ↓
# 内部任务继续运行

# 直接 task.cancel()
#    ↓
# 内部 Task 被取消

# wait_for()
# wait_for
#    ↓
# 超时
#    ↓
# cancel()
#    ↓
# save_data 被取消

import asyncio


async def work():
    try:
        print('work 开始')

        await asyncio.sleep(5)

        print('work 完成')
        return 'OK'

    except asyncio.CancelledError:
        print('work 被取消')
        raise


async def main():
    task = asyncio.create_task(work())

    try:
        result = await asyncio.wait_for(
            asyncio.shield(task),
            timeout=2
        )

        print('result:', result)

    except asyncio.TimeoutError:
        print('超时')

    print('task.done():', task.done())
    print('task.cancelled():', task.cancelled())

    await asyncio.sleep(4)

    print('task.done():', task.done())
    print('task.cancelled():', task.cancelled())

    print('main 结束')


asyncio.run(main())

# 1. 
# work 会不会开始？
# 会开始

# 2. 
# 2 秒后，wait_for 会发生什么？会不会抛 TimeoutError？
# 结束外层任务；
# 2 秒后仍然会抛 TimeoutError。
# shield() 保护的是：
# 内部的 task 不被取消
# 它不会阻止 wait_for() 超时。
# work 开始
#     ↓
# 等待 2 秒
#     ↓
# wait_for 超时
#     ↓
# TimeoutError
#     ↓
# except asyncio.TimeoutError
#     ↓
# 打印：超时

# 3. 
# 超时以后，work 会不会被取消？为什么？
# 会；因为shield，子任务没被取消； shield() 防止的是取消传播，不是防止超时。

# 4. 
# 第一次打印：
# task.done()
# task.cancelled()
# 分别是什么？
# False; False
# task.done()表示：Task 有没有结束。
# task.cancelled()表示：Task 最终是不是以“取消”状态结束。

# 5. 
# 再等待 4 秒后：
# task.done()
# task.cancelled()
# 分别是什么？
# True; False

# 6. 
# 最后会不会打印：
# work 完成
# main 结束
# 都会打印

# asyncio.wait_for() vs asyncio.timeout()
# asyncio.wait_for() 
# 给某一个 awaitable 设置超时时间
# asyncio.timeout()
# 给这一段代码设置一个 x 秒的超时时间

# wait_for
# └── 一个 awaitable

# timeout
# └── 一个代码块
#     ├── await A
#     ├── await B
#     └── await C

import asyncio


async def work(name, delay):
    try:
        print(f'{name} 开始')

        await asyncio.sleep(delay)

        print(f'{name} 完成')

        return name

    except asyncio.CancelledError:
        print(f'{name} 被取消')
        raise


async def main():
    task = asyncio.create_task(
        work('A', 5)
    )

    try:
        async with asyncio.timeout(2):
            result = await asyncio.shield(task)
            print('结果:', result)

    except asyncio.TimeoutError:
        print('超时')

    print('done:', task.done())
    print('cancelled:', task.cancelled())

    await asyncio.sleep(4)

    print('done:', task.done())
    print('cancelled:', task.cancelled())

    print('main 结束')


asyncio.run(main())

# 1. 
# A 会不会开始？
# 会

# 2. 
# 2 秒后，会不会进入：
#    except asyncio.TimeoutError？
# 会

# 3. 
# timeout 超时后，A 会不会被取消？
# 为什么？
# 不会取消；因为shield，shield() 阻止这个取消继续传递给内部 task

# 4. 
# 第一次：
# done:
# cancelled:
# 分别是什么？
# False False 

# 5. 
# 再等待 4 秒后：
# done:
# cancelled:
# 分别是什么？
# True False 

# 6. 
# 最终输出中：
# A 完成 超时 main 结束
# 这三个都会出现吗？
# 都会出现

# 7. 
# 如果把：
# await asyncio.shield(task)
# 改成：await task
# 那么超时后 A 会发生什么？
# A取消任务

# asyncio.as_completed()
# 让你按照“完成顺序”一个一个拿结果
# 适合并发请求多个接口，然后谁先返回就先处理谁的结果
# as_completed() 不会因为其中一个任务异常，就自动取消其他任务。
#                     asyncio
#                        │
#         ┌──────────────┴──────────────┐
#         ↓                             ↓
#       wait()                    as_completed()
#         │                             │
#         ↓                             ↓
#   done / pending              完成一个处理一个
#         │                             │
#         ↓                             ↓
# FIRST_COMPLETED              B → C → A
# FIRST_EXCEPTION
# ALL_COMPLETED
# wait() 更适合“观察一组任务当前处于什么状态”；as_completed() 更适合“按完成顺序消费任务结果”。

import asyncio


async def work(name, delay, error=False):
    print(f'{name} 开始')

    await asyncio.sleep(delay)

    if error:
        print(f'{name} 出错')
        raise ValueError(f'{name} error')

    print(f'{name} 完成')

    return name


async def main():
    tasks = [
        asyncio.create_task(work('A', 3)),
        asyncio.create_task(work('B', 1, True)),
        asyncio.create_task(work('C', 2)),
    ]

    for future in asyncio.as_completed(tasks):
        try:
            result = await future
            print('结果:', result)

        except Exception as e:
            print('捕获异常:', type(e).__name__)

    print('main 结束')


asyncio.run(main())

# 1.
# A、B、C 会不会全部开始？
# 会

# 2.
# 三个任务的完成/异常顺序是什么？
# 第一个：B 异常
# 第二个：C 正常
# 第三个：A 正常

# 3.
# as_completed() 返回的顺序，是：A,B
# A. 创建顺序 A → B → C
# B. 完成顺序 B → C → A
# C. 随机顺序

# 4.
# B 抛出 ValueError 后：except Exception as e:会不会捕获？
# 会捕获

# 5.
# B 出错以后，C 和 A 会不会继续运行？
# 会继续运行

# 6.
# 最终大概输出什么？(as_completed完成一个处理一个)
# A 开始
# B 开始
# C 开始
# B 出错
# 捕获异常: ValueError
# C 完成
# 结果:C
# A 完成
# 结果:A
# main 结束

# 7.
# 如果把：asyncio.as_completed(tasks)换成：
# await asyncio.wait(
#     tasks,
#     return_when=asyncio.FIRST_COMPLETED
# )
# 那么最大的区别是什么？
# 这一次 wait 返回时，还没有得到另外两个结果

# | 方法               | 核心特点            |
# | ---------------- | --------------- |
# | `gather()`       | **我要所有结果**      |
# | `wait()`         | **我要知道任务现在的状态** |
# | `as_completed()` | **谁先完成，我先处理谁**  |

# as_completed() 的 timeout
# as_completed(timeout=x) 的意思是：最多等 x秒，如果 x 秒内所有任务没有全部完成，就产生 TimeoutError。
# 超时后，其他 Task 会不会自动取消？不会。
# | 方法               | 核心特点                 |
# | ---------------- | -------------------- |
# | `gather()`       | 我要所有结果               |
# | `wait()`         | 我要知道谁 done、谁 pending |
# | `as_completed()` | 谁先完成，我先处理谁           |
# | `wait_for()`     | 给一个 awaitable 设置超时   |
# | `timeout()`      | 给一整段代码设置超时           |

# gather
#     ↓
# 我要全部结果

# wait
#     ↓
# 告诉我 done / pending

# as_completed
#     ↓
# 谁先完成先给谁

# wait_for
#     ↓
# 这个 await 最多等多久

# timeout
#     ↓
# 这一整段代码最多执行多久

# shield
#     ↓
# 外层取消/超时时，不要顺便取消内部 Task

async def work(name, seconds):
    print(name, '开始')
    await asyncio.sleep(seconds)
    print(name, '结束')
    return name


async def main():
    tasks = [
        asyncio.create_task(work('A', 3)),
        asyncio.create_task(work('B', 1)),
        asyncio.create_task(work('C', 5)),
    ]

    try:
        for future in asyncio.as_completed(tasks, timeout=2):
            result = await future
            print('结果:', result)
    except asyncio.TimeoutError:
        print('超时')

# 1.
# A、B、C 会不会都开始？
# 会

# 2.
# 1 秒时会发生什么？输出顺序是什么？
# B结束
# 结果:B

# 3.
# 结果: B 会不会打印？
# 会

# 4.
# 2 秒时会发生什么？A 和 C 会不会自动取消？
# 2秒内所有任务没有全部完成，就产生 TimeoutError。
# 不会

# 5.
# 如果把 as_completed() 换成：
# done, pending = await asyncio.wait(
#     tasks,
#     timeout=2
# )
# 2 秒后 done 和 pending 大概分别是什么？
# done B
# pending A C

# 6.
# 如果业务要求“2 秒内谁返回就用谁，剩余任务全部取消”，你会选择 as_completed() 还是 wait()？为什么？
# as_completed;因为wait还会返回pending 业务不关心pending的；只关心2秒内的

#                     并发任务
#                        │
#        ┌───────────────┼────────────────┐
#        │               │                │
#     gather          wait          as_completed
#        │               │                │
#     全部结果        done/pending       完成顺序
#        │               │                │
#     输入顺序        可以 timeout       谁先完成先处理

# wait_for
#    ↓
# 限制一个 awaitable 的时间

# timeout
#    ↓
# 限制一整段代码的时间

# shield
#    ↓
# 保护内部 Task 不被外层取消

import asyncio


async def tool(name, seconds):
    print(name, '开始')
    await asyncio.sleep(seconds)
    print(name, '完成')
    return name


async def main():
    tasks = [
        asyncio.create_task(tool('RAG', 3)),
        asyncio.create_task(tool('Search', 1)),
        asyncio.create_task(tool('DB', 2)),
    ]

    done, pending = await asyncio.wait(
        tasks,
        timeout=1.5
    )

    print('done:', len(done))
    print('pending:', len(pending))

# 1. 
# RAG、Search、DB 会不会都开始？
# 会

# 2. 
# 1.5 秒时，哪个任务在 done？
# Search

# 3. 
# 哪两个任务在 pending？
# RAG DB
# 4. 
# wait(timeout=1.5) 超时后，会不会自动取消 RAG 和 DB？
# 不会

# 5. 
# 如果业务改成：
# “三个工具全部完成后，我才能继续生成最终答案。”
# 你选择 gather、wait 还是 as_completed？为什么？
# gather 全部完成

# 6. 
# 如果业务改成：
# “三个工具同时执行，谁最先返回就直接使用谁，其他工具全部取消。”
# 你选择哪个？为什么？
# as_completed  最先返回就直接使用谁

# 7. 
# 如果业务改成：
# “最多等待 1.5 秒，1.5 秒时已经完成的全部拿来用，没完成的全部取消。”
# 你会怎么组合 wait() + cancel() + gather()？
# 先用wait拿到done和pending
# pendin的取消
# gather 收尾
# wait
#  ↓
# 得到 done / pending
#  ↓
# 处理 done
#  ↓
# cancel pending
#  ↓
# gather pending
#  ↓
# 完成清理
