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