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