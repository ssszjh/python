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