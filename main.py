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
    await asyncio.sleep(2)
    

asyncio.run(main())