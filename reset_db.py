import asyncio

from bot.database import engine, metadata


async def start_db():
    #перенести создание в докерфайл!!!
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)


if __name__ == "__main__":
    asyncio.run(start_db())