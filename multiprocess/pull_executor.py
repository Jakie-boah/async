import time
from concurrent.futures import ProcessPoolExecutor
import asyncio
from functools import partial
from typing import List
from asyncio.events import AbstractEventLoop


def count(count_to: int) -> int:
    start = time.time()
    counter = 0

    while counter < count_to:
        counter += 1

    end = time.time()
    print(f"Закончил подсчет до {count_to} за время {end - start}")
    return counter


async def main():
    with ProcessPoolExecutor() as process_pool:
        loop: AbstractEventLoop = asyncio.get_running_loop()
        nums = [1, 3, 5, 22, 100000000]
        calls: List[partial[int]] = [partial(count, num) for num in nums]
        call_coros = []

        for call in calls:
            call_coros.append(loop.run_in_executor(process_pool, call))

        results = await asyncio.gather(*call_coros)

        for result in results:
            print(result)


if __name__ == '__main__':
    asyncio.run(main())
