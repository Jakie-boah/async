import asyncio
import asyncpg
from loguru import logger
from asyncpg.transaction import Transaction


async def main():
    connection = await asyncpg.connect(
        host="localhost",
        port=5432,
        database="postgres",
        user="postgres",
        password="postgres",
    )

    async with connection.transaction():
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'brand_1')")
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'brand_2')")

    query = """
        SELECT brand_name FROM brand WHERE brand_name LIKE 'brand%'
        """
    brands = await connection.fetch(query)
    logger.info(brands)
    await connection.close()


async def main_error_handling():
    connection = await asyncpg.connect(
        host="localhost",
        port=5432,
        database="postgres",
        user="postgres",
        password="postgres",
    )
    try:
        async with connection.transaction():
            insert_brand = "INSERT INTO brand VALUES(9999, 'small_brand')"
            await connection.execute(insert_brand)
            await connection.execute(insert_brand)
    except Exception as e:
        logger.exception(e)
    finally:
        query = """
                SELECT brand_name FROM brand WHERE brand_name LIKE 'small%'
                """
        brands = await connection.fetch(query)
        logger.info(brands)
        await connection.close()


# asyncio.run(main_error_handling())


async def nested_transaction():
    connection = await asyncpg.connect(
        host="localhost",
        port=5432,
        database="postgres",
        user="postgres",
        password="postgres",
    )
    async with connection.transaction():
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'my_new_brand')")
        try:
            async with connection.transaction():
                await connection.execute("INSERT INTO product_color VALUES(1, 'black')")
        except Exception as ex:
            logger.warning(
                "Ошибка при вставке цвета товара игнорируется - {}".format(ex)
            )

    await connection.close()


# asyncio.run(nested_transaction())


async def manual_transaction():
    connection = await asyncpg.connect(
        host="localhost",
        port=5432,
        database="postgres",
        user="postgres",
        password="postgres",
    )
    transaction: Transaction = connection.transaction()
    await transaction.start()
    try:
        await connection.execute("INSERT INTO brand " "VALUES(DEFAULT, 'brand_1')")
        await connection.execute("INSERT INTO brand " "VALUES(DEFAULT, 'brand_2')")
    except asyncpg.PostgresError:
        logger.error("Ошибка! транзакция откатывается")

    else:
        logger.info("Ошибки нет! транзакция фиксируется")
        await transaction.commit()
    query = """SELECT brand_name FROM brand
    WHERE brand_name LIKE 'brand%'"""
    brands = await connection.fetch(query)
    logger.info(brands)
    await connection.close()


asyncio.run(manual_transaction())
