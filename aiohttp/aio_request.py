import asyncio
import aiohttp
from util import async_timed, fetch_status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = 'http://example.com'
        status = await fetch_status(session, url)
        print(f'Состояние для {url} было равно {status}')


@async_timed()
async def main_advanced():
    async with aiohttp.ClientSession() as session:
        urls = ['http://example.com' for _ in range(1000)]
        requests = [fetch_status(session, url) for url in urls]
        status_codes = await asyncio.gather(*requests)
        print(status_codes)


asyncio.run(main_advanced())
