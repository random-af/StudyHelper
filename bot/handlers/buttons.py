import logging

import sqlalchemy
from sqlalchemy.dialects.sqlite import insert
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

import config
import senders.keyboards as keyboards
import utils as utils
from database import users_tg, user_settings, execute, fetch_one


async def set_language_to_study(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = await utils.get_or_create_user(update)
    query = update.callback_query
    data = query.data.split("|")
    if data[-1] == "":
        text, reply_markup = keyboards.set_language_to_study()
        await query.edit_message_text(text, reply_markup=reply_markup)
    else:
        if data[-1] in config.LANGUAGES:
            statement = sqlalchemy.update(user_settings).where(user_settings.c.id == user["id"]).values(language=data[-1])
            await execute(statement)
            settings = await fetch_one(sqlalchemy.select(user_settings).where(user_settings.c.id == user["id"]))
            text, reply_markup = keyboards.menu(settings["mode"], settings["language"])
            await query.edit_message_text(text, reply_markup=reply_markup)
        else:
            raise NotImplementedError(f"no {data[-1]} among available languages")


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = await utils.get_or_create_user(update)
    settings = await fetch_one(sqlalchemy.select(user_settings).where(user_settings.c.id == user["id"]))
    query = update.callback_query
    text, reply_markup = keyboards.menu(settings["mode"], settings["language"])
    await query.edit_message_text(text, reply_markup=reply_markup)


async def modes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await utils.get_or_create_user(update)
    query = update.callback_query
    data = query.data.split("|")
    if data[-1] == "":
        text, reply_markup = keyboards.modes()
        await query.edit_message_text(text, reply_markup=reply_markup)
    elif data[-1] == "text_translations":
        text, reply_markup = keyboards.back_to_menu("Switched to text translations mode")
        await query.edit_message_text(text, reply_markup=reply_markup)
    else:
        raise NotImplementedError(data[-1])
    
async def text_translations(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await utils.get_or_create_user(update)
    query = update.callback_query
    data = query.data.split("|")
    if data[-1] == "start":
        pass
    elif data[-1] == "statistics":
        pass
    elif data[-1] == "add_questions":
        pass
    else:
        raise NotImplementedError(data[-1])
