import random
from tasks import add
from decouple import config
from concurrent.futures import ThreadPoolExecutor
import asyncio
from utils import Timer

QNT_TASKS = config('QNT_TASKS', default=1000, cast=int)


async def call(executor, num, futs):
    print(num)
    futs.append(executor.submit(add.delay, random.randint(1, 100),
                                random.randint(-100, 1)))


async def run():
    futs = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        await asyncio.gather(*[call(executor, n, futs)
                             for n in range(QNT_TASKS)])
        results = [fut.result() for fut in futs]


if __name__ == '__main__':

    with Timer() as t:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run())

    print('Job took %.03f sec.' % t.interval)
