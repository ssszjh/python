# 1.Timeout 和 Cancellation 到底是什么关系
# 2.asyncio.wait_for() vs asyncio.timeout()：区别与选择
# 3.Timeout + Cancellation + finally：放到 HTTP / LLM / Agent 场景理解

        #      wait_for
        #         │
        #         │ timeout = 2s
        #         ↓
        #      cancel
        #         │
        #         ↓
        #   ┌─────────────┐
        #   │    work     │
        #   │             │
        #   │ CancelledError
        #   └──────┬──────┘
        #          │
        #          ↓
        #       raise
        #          │
        #          ↓
        # wait_for 感知取消
        #          │
        #          ↓
        #   TimeoutError
        #          │
        #          ↓
        #      外层捕获

# CancelledError 是取消过程中的内部信号，TimeoutError 是 Timeout API 对外表达的结果。

# | Python       | 关注点            |
# | ------------ | -------------- |
# | `wait_for()` | 一个具体 awaitable |
# | `timeout()`  | 一段代码 / 一个时间预算  |

# timeout 包裹谁
#      ↓
# 谁受到 timeout 控制
#      ↓
# 超时后谁会进入 cancellation 流程

#                 Timeout
#                    │
#                    ↓
#               请求 Cancel
#                    │
#                    ↓
#           CancelledError 注入
#                    │
#                    ↓
#              finally cleanup
#                    │
#                    ↓
#             Task 真正结束
#                    │
#                    ↓
#         Timeout API 对外表现
#                    │
#                    ↓
#              TimeoutError

# wait_for()
#     ↓
# 控制一个具体 awaitable
#     ↓
# “这个请求最多 X 秒”


# timeout()
#     ↓
# 控制一个代码块
#     ↓
# “这段业务总共最多 X 秒”

1.
import asyncio

async def work():
    try:
        print('A')
        await asyncio.sleep(5)
        print('B')
    except asyncio.CancelledError:
        print('C')
        raise
    finally:
        print('D')

async def main():
    task = asyncio.create_task(work())

    try:
        await asyncio.wait_for(task, timeout=1)
    except asyncio.TimeoutError:
        print('E')

    print('done:', task.done())
    print('cancelled:', task.cancelled())

asyncio.run(main())

# 1.输出顺序是什么？  A C D E done:True cancelled:True
# 2.task.done() 是什么？ True
# 3.task.cancelled() 是什么？ True
# 4.wait_for 超时后，task 是谁被取消？ task，也就是 work() 对应的 Task 被请求取消。