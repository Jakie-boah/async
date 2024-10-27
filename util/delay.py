import asyncio


async def delay(delay_seconds: int) -> int:
    print(f"Засыпаю на {delay_seconds} c")
    await asyncio.sleep(delay_seconds)
    print(f"сон в течение {delay_seconds} c закончился")
    return delay_seconds
