from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, select
from telegram_bot.telegram_model import engine
from telegram_bot import start

from telegram_bot.telegram_model import TelegramUser, Bundle, Question
from utils import load_or_create_user


reply_keyboard = [
    ["Start"],
    ["Select bundle", "Edit bundle"],
    ["Stop"],

]
menu_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE, db_session):
    callback_query = update.callback_query.data
    if callback_query == 'create bundle':
        context.user_data['status'] = 'new bundle'
        context.user_data['stage'] = 'naming'
        await update.callback_query.edit_message_text(text="Enter new bundle name:")
    elif callback_query == 'help':
        await update.callback_query.edit_message_text(text="[Dev] here help message pops up") # obedinit vse help v odnu funcciu
    else:
        context.user_data.clear()
        context.user_data['status'] = 'menu'
        context.user_data['stage'] = ''
        await update.message.reply_text('Done', reply_markup=menu_markup)


async def new_bundle(update: Update, context: ContextTypes.DEFAULT_TYPE, db_session):
    callback_query = update.callback_query.data
    if callback_query == 'add questions (type in chat)':
        context.user_data['status'] = 'new question'
        context.user_data['stage'] = 'entering question'
        await update.callback_query.edit_message_text(text="Enter question:")
    elif callback_query == 'add questions (question ; answer)':
        context.user_data['status'] = 'new question'
        context.user_data['stage'] = 'entering question ; answer'
        await update.callback_query.edit_message_text(text="Enter question ; answer sequence\n"
                                                           "(each pair must start on different line):")
    elif callback_query == 'menu':
        context.user_data.clear()
        context.user_data['status'] = 'menu'
        context.user_data['stage'] = ''
        await update.message.reply_text('Done', reply_markup=menu_markup)


async def selecting_bundle(update: Update, context: ContextTypes.DEFAULT_TYPE, db_session):
    callback_query = update.callback_query.data
    splited = callback_query.split(' ')
    user_id = update.effective_chat.id
    user = load_or_create_user(user_id, db_session)
    user.current_bundle_id = int(splited[-1])
    db_session.commit()
    context.user_data.clear()
    context.user_data['status'] = 'menu'
    context.user_data['stage'] = ''
    await update.callback_query.edit_message_text(text=f'Switched to bundle "{splited[-2]}"')


async def new_question(update: Update, context: ContextTypes.DEFAULT_TYPE, db_session):
    callback_query = update.callback_query.data
    if callback_query == 'add questions (type in chat)':
        context.user_data['stage'] = 'entering question'
        await update.callback_query.edit_message_text(text="Enter question:")
    elif callback_query == 'add questions (question ; answer)':
        context.user_data['stage'] = 'entering question ; answer'
        await update.callback_query.edit_message_text(text="Enter question ; answer sequence\n"
                                                           "(each pair must start on different line):")
    elif callback_query == 'menu':
        context.user_data.clear()
        context.user_data['status'] = 'menu'
        context.user_data['stage'] = ''
        await update.message.reply_text('Done adding questions', reply_markup=menu_markup)
    elif callback_query == 'edit question':
        context.user_data.clear()
        context.user_data['status'] = 'menu'
        context.user_data['stage'] = ''
        await update.callback_query.edit_message_text(text="[Dev] Coming up soon...")


async def editing_bundle(update: Update, context: ContextTypes.DEFAULT_TYPE, db_session):
    callback_query = update.callback_query.data
    if callback_query == 'add questions (type in chat)':
        context.user_data['status'] = 'new question'
        context.user_data['stage'] = 'entering question'
        await update.callback_query.edit_message_text(text="Enter question:")
    elif callback_query == 'add questions (question ; answer)':
        context.user_data['status'] = 'new question'
        context.user_data['stage'] = 'entering question ; answer'
        await update.callback_query.edit_message_text(text="Enter question ; answer sequence\n"
                                                           "(each pair must start on different line):")
    elif callback_query == 'edit questions':
        context.user_data.clear()
        context.user_data['status'] = 'menu'
        context.user_data['stage'] = ''
        await update.callback_query.edit_message_text(text="[Dev] Coming up soon...")
    elif callback_query == 'rename bundle':
        context.user_data['status'] = 'editing bundle'
        context.user_data['stage'] = 'renaming bundle'
        await update.callback_query.edit_message_text(text="Enter bundle name:")
        #await update.message.reply_text("Enter bundle name:")
    elif callback_query == 'delete bundle':
        context.user_data['stage'] = 'deleting bundle'
        keyboard = [[InlineKeyboardButton("Yes", callback_data="delete bundle yes"), ],
                    [InlineKeyboardButton("No", callback_data="delete bundle no"), ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.edit_message_text(f'Are you sure you want to delete bundle {context.user_data["bundle"].name}?',
                                        reply_markup=reply_markup)
    elif callback_query == 'delete bundle yes':
        bundle_name = context.user_data["bundle"].name
        db_session.delete(context.user_data["bundle"])
        user_id = update.effective_chat.id
        user = load_or_create_user(user_id, db_session)
        user.current_bundle_id = None
        db_session.commit()
        context.user_data['status'] = 'menu'
        context.user_data['stage'] = ''
        await update.callback_query.edit_message_text(f'bundle {bundle_name} was deleted!')
    elif callback_query == 'delete bundle no':
        context.user_data.clear()
        context.user_data['status'] = 'menu'
        context.user_data['stage'] = ''
        await update.message.reply_text('Done', reply_markup=menu_markup)
    elif callback_query == 'menu':
        context.user_data.clear()
        context.user_data['status'] = 'menu'
        context.user_data['stage'] = ''
        await update.message.reply_text('Done', reply_markup=menu_markup)


async def studying(update: Update, context: ContextTypes.DEFAULT_TYPE, db_session, question_selector):
    pass

