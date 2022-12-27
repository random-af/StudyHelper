from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, select
from telegram_bot.telegram_model import engine
from telegram_bot import start

import process_message_func
import button_pressed_func
from telegram_bot.telegram_model import TelegramUser, Bundle, Question
from utils import load_or_create_user
from question_selector import RandomSelector


Session = sessionmaker(bind=engine)  # creating database session
db_session = Session()
question_selector = RandomSelector(db_session)


# ---- REPLY HANDLERS----

async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('status', 'menu') == 'menu':
        await process_message_func.menu(update, context, db_session)
    elif context.user_data.get('status', 'menu') == 'new bundle':
        await process_message_func.new_bundle(update, context, db_session)
    elif context.user_data.get('status', 'menu') == 'selecting bundle':
        await process_message_func.selecting_bundle(update, context, db_session)
    elif context.user_data.get('status', 'menu') == 'new question':
        await process_message_func.new_question(update, context, db_session)
    elif context.user_data.get('status', 'menu') == 'editing bundle':
        await process_message_func.editing_bundle(update, context, db_session)
    elif context.user_data.get('status', 'menu') == 'studying':
        await process_message_func.studying(update, context, db_session, question_selector)


async def button_pressed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('status', 'menu') == 'menu':
        await button_pressed_func.menu(update, context, db_session)
    elif context.user_data.get('status', 'menu') == 'new bundle':
        await button_pressed_func.new_bundle(update, context, db_session)
    elif context.user_data.get('status', 'menu') == 'selecting bundle':
        await button_pressed_func.selecting_bundle(update, context, db_session)
    elif context.user_data.get('status', 'menu') == 'new question':
        await button_pressed_func.new_question(update, context, db_session)
    elif context.user_data.get('status', 'menu') == 'editing bundle':
        await button_pressed_func.editing_bundle(update, context, db_session)
    elif context.user_data.get('status', 'menu') == 'studying':
        await button_pressed_func.studying(update, context, db_session, question_selector)


# ----COMMAND HANDLERS----

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    user = load_or_create_user(user_id, db_session)
    #bundle_count = db_session.query(func.count(Bundle)).where(Bundle.user_id == user_id) # pochemu ne rabotaet???
    stmt = select(func.count()).select_from(Bundle).where(Bundle.user_id == user_id)
    bundle_count = db_session.execute(stmt).first()[0]
    if user.current_bundle_id is not None:
        context.user_data['status'] = 'studying'
        context.user_data['stage'] = 'answering'
        question = question_selector.get_question(user.current_bundle_id)
        context.user_data['question'] = question
        await update.message.reply_text(text=f'question: {question.question}')
        #todo: add studying
    elif bundle_count != 0:
        #context.user_data['status'] = 'selecting bundle'
        #todo: add selecting bundle
        await update.message.reply_text("Bundle is not selected use /select_bundle first")
    else:
        #todo: add creating bundle
        keyboard = [
            [InlineKeyboardButton("Create Bundle", callback_data="create bundle"),
             InlineKeyboardButton("Help", callback_data="help")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Seems like you don't have any bundle", reply_markup=reply_markup)


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data['status'] = 'menu'
    context.user_data['stage'] = ''
    await update.message.reply_text('Stopped', reply_markup=button_pressed_func.menu_markup)


async def select_bundle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    #user = load_or_create_user(user_id)
    stmt = select(func.count()).select_from(Bundle).where(Bundle.user_id == user_id)
    bundle_count = db_session.execute(stmt).first()[0]
    if bundle_count > 0:
        context.user_data['status'] = 'selecting bundle'
        context.user_data['stage'] = ''
        keyboard = []
        # bundles = db_session.execute(select(Bundle).where(Bundle.id == user.current_bundle_id))
        bundles = db_session.query(Bundle).filter(Bundle.user_id == user_id)
        for bundle in bundles:
            keyboard.append(
                [InlineKeyboardButton(bundle.name, callback_data=f"selecting bundle {bundle.name} {bundle.id}")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Select bundle:", reply_markup=reply_markup)
    else:
        # todo: add creating bundle
        keyboard = [
            [InlineKeyboardButton("Create Bundle", callback_data="create bundle"),
             InlineKeyboardButton("Help", callback_data="help")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Seems like you don't have any bundle", reply_markup=reply_markup)


async def edit_bundle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    user = load_or_create_user(user_id, db_session)
    bundle_id = user.current_bundle_id
    if bundle_id is None:
        await update.message.reply_text("Bundle is not selected use /select_bundle first")
    else:
        bundle = db_session.query(Bundle).filter(Bundle.id == user.current_bundle_id).first()
        context.user_data['status'] = 'editing bundle'
        context.user_data['stage'] = ''
        context.user_data['bundle'] = bundle
        keyboard = [
            [InlineKeyboardButton("Add questions (type in chat)", callback_data="add questions (type in chat)"), ],
            [InlineKeyboardButton("Add questions (question ; answer)",
                                  callback_data="add questions (question ; answer)"), ],
            [InlineKeyboardButton("Edit questions", callback_data="edit questions"), ],
            [InlineKeyboardButton("Rename bundle", callback_data="rename bundle"), ],
            [InlineKeyboardButton("Delete bundle", callback_data="delete bundle"), ],
            [InlineKeyboardButton("Cancel", callback_data="menu"), ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(f"Editing bundle {bundle.name}:", reply_markup=reply_markup)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data['status'] = 'menu'
    context.user_data['stage'] = ''
    await update.message.reply_text('[Dev] here help message pops up', reply_markup=button_pressed_func.menu_markup)


def main():
    application = Application.builder().token("5982143169:AAExh6WNAWuMoFO8fMHeEGSZN88L8BiUf-Y").build()
    # ubrat token v env variable !!!!!!!!!!!!!!!!!!!!

    # dobavit' logger !!!!!!!!!!!!!!!!!!

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('stop', stop))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('select_bundle', select_bundle))
    application.add_handler(CommandHandler('edit_bundle', edit_bundle))
    application.add_handler(MessageHandler(filters.Regex("Start"), start))
    application.add_handler(MessageHandler(filters.Regex("Stop"), stop))
    application.add_handler(MessageHandler(filters.Regex("Select bundle"), select_bundle))
    application.add_handler(MessageHandler(filters.Regex("Edit bundle"), edit_bundle))
    application.add_handler(CallbackQueryHandler(button_pressed))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message))

    print('run')
    application.run_polling()


if __name__ == '__main__':
    main()
