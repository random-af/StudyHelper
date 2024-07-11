import logging

from sqlalchemy import select
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

import senders.keyboards as keyboards
import utils

import config
from database import fetch_one, user_settings


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await utils.get_or_create_user(update)
    settings = await fetch_one(select(user_settings).where(user_settings.c.id == user["id"]))  # change to get_or_create_user_settings()
    text, reply_markup = keyboards.menu(settings["mode"], settings["language"])
    await update.message.reply_text(text, reply_markup=reply_markup)
