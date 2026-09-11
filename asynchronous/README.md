异步编程 

async def
   ↓
Coroutine（协程）
   ↓
await
   ↓
Event Loop（事件循环）
   ↓
asyncio.run()
   ↓
Task
   ↓
并发执行 asyncio.gather()
   ↓
asyncio.create_task()
   ↓
同步代码 vs 异步代码
Future Coroutine
异步异常处理
TaskGroup
asyncio.wait
wait_for
asyncio.as_completed()
   ↓
异步 IO：网络请求 / 文件 / 数据库
   ↓
异步生成器 async for / async yield
   ↓
异步上下文管理器 async with
   ↓
实际项目中的异步编程