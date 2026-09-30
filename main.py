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