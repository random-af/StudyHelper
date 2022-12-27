from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, select
from telegram_bot.telegram_model import engine
from telegram_bot import start

from telegram_bot.telegram_model import TelegramUser, Bundle, Question
from utils import load_or_create_user


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE, db_session):
    pass


async def new_bundle(update: Update, context: ContextTypes.DEFAULT_TYPE, db_session):
    #mb dobavit' proverku na stage
    user_id = update.effective_chat.id
    user = load_or_create_user(user_id, db_session)
    text = update.message.text
    # todo: check name for constraints
    new_bundle = Bundle(user_id=user_id, name=text)  # dobavit' proverku na format texta !!!!!!!
    db_session.add(new_bundle)
    user.current_bundle_id = new_bundle.id
    db_session.commit()
    context.user_data['bundle'] = new_bundle
    context.user_data['status'] = 'new question' # horosho li tak delat'??
    context.user_data['stage'] = ''
    keyboard = [
        [InlineKeyboardButton("Add questions (type in chat)", callback_data="add questions (type in chat)"), ],
        [InlineKeyboardButton("Add questions (question ; answer)",
                              callback_data="add questions (question ; answer)"), ],
        [InlineKeyboardButton("Will do it later", callback_data="menu"), ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("You have created new bundle!\n"
                                    "Now it's empty. To start using it you need to add some questions",
                                    reply_markup=reply_markup)


async def selecting_bundle(update: Update, context: ContextTypes.DEFAULT_TYPE, db_session):
    pass


async def new_question(update: Update, context: ContextTypes.DEFAULT_TYPE, db_session):
    text = update.message.text
    if context.user_data['stage'] == 'entering question':
        # todo: check question for constraints
        new_question = Question(bundle_id=context.user_data['bundle'].id,
                                question=text)  # dobavit' proverku na format texta !!!!!!!
        # context.user_data['question_id'] = new_id
        context.user_data['question'] = new_question
        # db_session.add(new_question)
        # db_session.commit()
        context.user_data['stage'] = 'enter answer'
        await update.message.reply_text('Enter answer:')
    elif context.user_data['stage'] == 'enter answer':
        new_question = context.user_data['question']
        new_question.answer = text
        db_session.add(new_question)
        db_session.commit()
        context.user_data['stage'] = '' # nuzhno ???
        keyboard = [
            [InlineKeyboardButton("Add another question", callback_data="add questions (type in chat)"), ],
            # [InlineKeyboardButton("Add questions (question ; answer)",
            #                       callback_data="add questions (question ; answer)"), ],
            [InlineKeyboardButton("Edit question", callback_data="edit question"), ],
            [InlineKeyboardButton("Go to menu", callback_data="menu"), ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(f"You've added\n"
                                        f"question: {new_question.question}\n"
                                        f"answer: {new_question.answer}",
                                        reply_markup=reply_markup)
    elif context.user_data['stage'] == 'entering question ; answer':
        for line in text.split('\n'):
            question, answer = line.split(';')
            new_question = Question(bundle_id=context.user_data['bundle'].id,
                                    question=question.strip(),
                                    answer=answer.strip())  # dobavit' proverku na format texta !!!!!!!
            db_session.add(new_question)
            db_session.commit()
    else:
        print('something wrong')
        context.user_data.clear()
        context.user_data['status'] = 'menu'
        context.user_data['stage'] = ''


async def editing_bundle(update: Update, context: ContextTypes.DEFAULT_TYPE, db_session):
    text = update.message.text
    if context.user_data['stage'] == 'renaming bundle':
        #todo: check for name constraints
        bundle = context.user_data['bundle']
        prev_name = bundle.name
        bundle.name = text
        db_session.commit()
        await update.message.reply_text(f'Bundle {prev_name} was successfully renamed to {text}')
    elif context.user_data['stage'] == '':
        pass


async def studying(update: Update, context: ContextTypes.DEFAULT_TYPE, db_session, question_selector):
    text = update.message.text
    user_id = update.effective_chat.id
    user = load_or_create_user(user_id, db_session)
    question = question_selector.get_question(user.current_bundle_id)
    answer = context.user_data["question"].answer
    context.user_data['question'] = question
    await update.message.reply_text(f'correct answer: {answer}\n\n'
                                    f'question: {question.question}')
