""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""

import os
import aiosqlite

DATABASE_PATH = f"{os.path.realpath(os.path.dirname(__file__))}/../database/database.db"


async def get_blacklisted_users() -> list:
    """
    This function will return the list of all blacklisted users.

    :param user_id: The ID of the user that should be checked.
    :return: True if the user is blacklisted, False if not.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT user_id, strftime('%s', created_at) FROM blacklist"
        ) as cursor:
            result = await cursor.fetchall()
            return result


async def is_blacklisted(user_id: int) -> bool:
    """
    This function will check if a user is blacklisted.

    :param user_id: The ID of the user that should be checked.
    :return: True if the user is blacklisted, False if not.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT * FROM blacklist WHERE user_id=?", (user_id,)
        ) as cursor:
            result = await cursor.fetchone()
            return result is not None


async def add_user_to_blacklist(user_id: int) -> int:
    """
    This function will add a user based on its ID in the blacklist.

    :param user_id: The ID of the user that should be added into the blacklist.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("INSERT INTO blacklist(user_id) VALUES (?)", (user_id,))
        await db.commit()
        rows = await db.execute("SELECT COUNT(*) FROM blacklist")
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0


async def remove_user_from_blacklist(user_id: int) -> int:
    """
    This function will remove a user based on its ID from the blacklist.

    :param user_id: The ID of the user that should be removed from the blacklist.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM blacklist WHERE user_id=?", (user_id,))
        await db.commit()
        rows = await db.execute("SELECT COUNT(*) FROM blacklist")
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0

async def set_channel(server_id: int, channel_id: int) -> None:
    """
    This function will set the channel where the bot speaks for a server.

    :param server_id: The ID of the server.
    :param channel_id: The ID of the channel.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO channels(server_id, channel_id) VALUES (?, ?)",
            (server_id, channel_id),
        )
        await db.execute(
            "UPDATE channels SET channel_id=? WHERE server_id=?",
            (channel_id, server_id),
        )
        await db.commit()


async def get_channel(server_id: int) -> int:
    """
    This function will get the channel where the bot speaks for a server.

    :param server_id: The ID of the server.
    :return: The ID of the channel.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT channel_id FROM channels WHERE server_id=?", (server_id,)
        ) as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else None
        
async def set_model(server_id: int, model: str) -> None:
    """
    This function will set the model for a server.

    :param server_id: The ID of the server.
    :param model: The model.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO models(server_id, model) VALUES (?, ?)",
            (server_id, model),
        )
        await db.execute(
            "UPDATE models SET model=? WHERE server_id=?",
            (model, server_id),
        )
        await db.commit()

async def get_model(server_id: int) -> str:
    """
    This function will get the model for a server.

    :param server_id: The ID of the server.
    :return: The model.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT model FROM models WHERE server_id=?", (server_id,)
        ) as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else None

async def opt_in(guild_id: int) -> None:
    """
    This function will opt a server in to conversation data collection.

    :param guild_id: The ID of the server.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO opt(guild_id, opt) VALUES (?, ?)",
            (guild_id, 1),
        )
        await db.execute(
            "UPDATE opt SET opt=? WHERE guild_id=?",
            (1, guild_id),
        )
        await db.commit()

async def opt_out(guild_id: int) -> None:
    """
    This function will opt a server out of conversation data collection, then wipe data collected from that server.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO opt(guild_id, opt) VALUES (?, ?)",
            (guild_id, 0),
        )
        await db.execute(
            "UPDATE opt SET opt=? WHERE guild_id=?",
            (0, guild_id),
        )
        await db.execute(
            "DELETE FROM messages WHERE guild_id=?",
            (guild_id,),
        )
        await db.commit()

async def get_opt(guild_id: int) -> int:
    """
    This function will get the opt status for a server.

    :param guild_id: The ID of the server.
    :return: The opt status.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT opt FROM opt WHERE guild_id=?", (guild_id,)
        ) as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else None

async def add_message(guild_id: int, author_id: int, channel_id: int, content: str) -> None:
    """
    This function will add a message to the database.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT INTO messages(guild_id, author_id, channel_id, content) VALUES (?, ?, ?, ?)",
            (guild_id, author_id, channel_id, content),
        )
        await db.commit()