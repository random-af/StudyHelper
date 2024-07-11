from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from database import fetch_one, execute, users_tg, user_settings
import config


def get_base_settings():
    return {"language": "english", "mode": "text_translations"}


async def get_user(id: int):
    statement = select(users_tg).where(users_tg.c.id == id)
    return await fetch_one(statement)


async def get_or_create_user(update: Update):
    effective_user = update.effective_user
    user_dict = {"id": effective_user.id,
                 "username": effective_user.username,
                 "first_name": effective_user.first_name,
                 "last_name": effective_user.last_name,
                 "is_premium": effective_user.is_premium,
                 "language_code": effective_user.language_code}
    user = await get_user(user_dict["id"])
    if user is None:
        await create_or_update_user(user_dict)
        user = await get_user(user_dict["id"])
        statement = insert(user_settings)\
            .values({"id": effective_user.id, "language": config.LANGUAGES[0], "mode": config.MODES[0]})
        await execute(statement)
    return user
     
     
async def create_or_update_user(user_dict: dict):
    user_dict.update({"updated_at": datetime.utcnow()})
    statement = insert(users_tg)\
        .values(user_dict)\
        .on_conflict_do_update(
                index_elements=(users_tg.c.id,),
                set_=user_dict,
            )
    return await execute(statement)