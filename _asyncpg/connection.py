import asyncio
import asyncpg
from loguru import logger
from _asyncpg.products import *


async def main():
    connection = await asyncpg.connect(
        host='localhost', port=5432, database='postgres', user='postgres',
        password='postgres'
    )
    statements = [CREATE_BRAND_TABLE,
                  CREATE_PRODUCT_TABLE,
                  CREATE_PRODUCT_COLOR_TABLE,
                  CREATE_PRODUCT_SIZE_TABLE,
                  CREATE_SKU_TABLE,
                  SIZE_INSERT,
                  COLOR_INSERT]

    logger.info('Создается база данных product...')
    for statement in statements:
        status = await connection.execute(statement)
    logger.info(status)
    logger.info('База данных product создана!')
    await connection.close()


asyncio.run(main())
