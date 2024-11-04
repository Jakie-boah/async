import asyncio
import aiohttp
from util import async_timed, fetch_status
from loguru import logger


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = "http://example.com"
        status = await fetch_status(session, url)
        print(f"Состояние для {url} было равно {status}")


@async_timed()
async def main_advanced():
    async with aiohttp.ClientSession() as session:
        urls = ["http://example.com" for _ in range(1000)]
        requests = [fetch_status(session, url) for url in urls]
        status_codes = await asyncio.gather(*requests)
        print(status_codes)


@async_timed()
async def gather_with_exception():
    async with aiohttp.ClientSession() as session:
        urls = ["http://example.com", "python://example.com"]
        tasks = [fetch_status(session, url) for url in urls]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        exceptions = [res for res in results if isinstance(res, Exception)]
        successful_results = [res for res in results if not isinstance(res, Exception)]

        print(f"Все результаты {results}")
        print(f"Ошибки: {exceptions}")
        print(f"Успех: {successful_results}")


@async_timed()
async def as_complete_usage():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            fetch_status(session, "http://example.com", 1),
            fetch_status(session, "http://example.com", 1),
            fetch_status(session, "http://example.com", 10),
        ]
        for finished_task in asyncio.as_completed(fetchers):
            print(await finished_task)


@async_timed()
async def as_completed_usage_timeout():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            fetch_status(session, "http://example.com", 1),
            fetch_status(session, "http://example.com", 10),
            fetch_status(session, "http://example.com", 10),
        ]
        for done_task in asyncio.as_completed(fetchers, timeout=2):
            try:
                print(await done_task)
            except TimeoutError:
                logger.error("Произошел тайм аут")

        for task in asyncio.tasks.all_tasks():
            logger.info(task)


@async_timed()
async def wait():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(
                fetch_status(
                    session,
                    "http://example.com",
                )
            ),
            asyncio.create_task(
                fetch_status(
                    session,
                    "http://example.com",
                )
            ),
            asyncio.create_task(
                fetch_status(
                    session,
                    "http://example.com",
                )
            ),
        ]

        done, pending = await asyncio.wait(fetchers)

        logger.info(f"Число завершившихся задач: {len(done)}")
        logger.info(f"Число ожидающих задач: {len(pending)}")

        for done_task in done:
            logger.info(await done_task)


@async_timed()
async def wait_error_handling():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(
                fetch_status(
                    session,
                    "http://example.com",
                )
            ),
            asyncio.create_task(
                fetch_status(
                    session,
                    "python://example.com",
                )
            ),
        ]

        done, pending = await asyncio.wait(fetchers)

        logger.info(f"Число завершившихся задач: {len(done)}")
        logger.info(f"Число ожидающих задач: {len(pending)}")

        for done_task in done:
            if done_task.exception() is None:
                logger.info(done_task.result())
            else:
                logger.error(done_task.exception())


@async_timed()
async def wait_error_handling_advanced():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(session, "python://bad.com")),
            asyncio.create_task(
                fetch_status(session, "https://www.example.com", delay=3)
            ),
            asyncio.create_task(
                fetch_status(session, "https://www.example.com", delay=3)
            ),
        ]

        done, pending = await asyncio.wait(
            fetchers, return_when=asyncio.FIRST_EXCEPTION
        )

        logger.info(f"Число завершившихся задач: {len(done)}")
        logger.info(f"Число ожидающих задач: {len(pending)}")

        for done_task in done:
            if done_task.exception() is None:
                logger.info(done_task.result())
            else:
                logger.error(done_task.exception())

        for pending_task in pending:
            logger.info("Останавливаю таск {}".format(pending_task))
            pending_task.cancel()


@async_timed()
async def wait_first_completed():
    async with aiohttp.ClientSession() as session:
        url = "http://example.com"

        fetchers = [
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url)),
        ]

        done, pending = await asyncio.wait(
            fetchers, return_when=asyncio.FIRST_COMPLETED
        )

        logger.info(f"Число завершившихся задач: {len(done)}")
        logger.info(f"Число ожидающих задач: {len(pending)}")

        for done_task in done:
            logger.info(await done_task)


@async_timed()
async def wait_first_complete_loop():
    async with aiohttp.ClientSession() as session:
        url = "http://example.com"
        pending = [
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url)),
        ]

        while pending:
            done, pending = await asyncio.wait(
                pending, return_when=asyncio.FIRST_COMPLETED
            )

            logger.info(f"Число завершившихся задач: {len(done)}")
            logger.info(f"Число ожидающих задач: {len(pending)}")

            for done_task in done:
                logger.info(await done_task)


asyncio.run(wait_first_complete_loop())
