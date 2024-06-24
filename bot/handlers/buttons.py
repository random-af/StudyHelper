import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

import senders.keyboards as keyboards


async def set_language_to_study(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = query.data.split("|")
    if data[-1] == "":
        text, reply_markup = keyboards.set_language_to_study()
        await query.edit_message_text(text, reply_markup=reply_markup)
    elif data[-1] == "english":
        text, reply_markup = keyboards.back_to_menu("Switched studyiung language to english")
        await query.edit_message_text(text, reply_markup=reply_markup)
    elif data[-1] == "spanish":
        text, reply_markup = keyboards.back_to_menu("Switched studyiung language to spanish")
        await query.edit_message_text(text, reply_markup=reply_markup)
    elif data[-1] == "other":
        text, reply_markup = keyboards.back_to_menu("Switched to other")
        await query.edit_message_text(text, reply_markup=reply_markup)
    else:
        raise NotImplementedError(data[-1])


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    text, reply_markup = keyboards.menu()
    await query.edit_message_text(text, reply_markup=reply_markup)


async def modes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
