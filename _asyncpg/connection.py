import asyncio
import asyncpg
from loguru import logger
from _asyncpg.products import *
from asyncpg import Record
from typing import List, Tuple
from random import sample


def load_common_words() -> List[str]:
    with open("common-words.txt") as f:
        return f.readlines()


def generate_brand_names(words: List[str]) -> List[Tuple[str,]]:
    return [(words[index],) for index in sample(range(100), 100)]


async def insert_brands(common_words, connection) -> int:
    brands = generate_brand_names(common_words)
    insert_brands = "INSERT INTO brand VALUES(DEFAULT, $1)"
    return await connection.executemany(insert_brands, brands)


async def main():
    common_words = load_common_words()
    connection = await asyncpg.connect(
        host="localhost",
        port=5432,
        database="postgres",
        user="postgres",
        password="postgres",
    )
    await insert_brands(common_words, connection)
    await connection.close()


asyncio.run(main())
