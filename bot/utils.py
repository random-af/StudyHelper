from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from database import fetch_one, execute, users_tg


def get_base_settings():
    return {"language": "english", "mode": "text_translations"}


async def get_user(id: int):
    statement = select(users_tg).where(users_tg.c.id == id)
    return await fetch_one(statement)


async def get_or_create_user(user_dict: dict):
    user = get_user(user_dict["id"])
    if user is None:
        return create_or_update_user(user_dict)
    else:
        return user
     
     
async def create_or_update_user(user_dict: dict):
    user_dict.update({"updated_at": datetime.utcnow()})
    statement = insert(users_tg)\
        .values(user_dict)\
        .on_conflict_do_update(
                index_elements=(users_tg.c.id,),
                set_=user_dict,
            )
    await execute(statement)