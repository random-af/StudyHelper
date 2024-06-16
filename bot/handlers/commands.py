import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

import senders.keyboards as keyboards


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text, reply_markup = keyboards.menu()
    await update.message.reply_text(text, reply_markup=reply_markup)
