import asyncio

async def work(name, delay):
    print(f'{name} 开始')

    await asyncio.sleep(delay)

    if name == 'B':
        raise ValueError('B 出错了')

    print(f'{name} 结束')
    
async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(work('A', 3))
        tg.create_task(work('B', 1))
        tg.create_task(work('C', 5))

    print('TaskGroup结束')

asyncio.run(main())