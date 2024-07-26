import logging
import os
import requests
import json

import flag
import sqlalchemy
from sqlalchemy.dialects.sqlite import insert
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, CallbackContext

import config

async def handle_message(update: Update, context: CallbackContext):
    message_handler = context.user_data.get("message_handler", "translation") #todo: add list of handlers
    text = update.message.text
    IAM_TOKEN = os.environ["IAM_TOKEN"]
    if message_handler == "translation":
        url = "https://translate.api.cloud.yandex.net/translate/v2/translate" #todo: add to config
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {IAM_TOKEN}"
        }
        data = {
            "folderId": "b1g9kk5ljc3ud347a2rd",
            "texts": [text],
            "targetLanguageCode": "ru",
        }
        response = requests.post(url, data=json.dumps(data), headers=headers)
        translation = json.loads(response.text)["translations"][0]
        translation_text = translation["text"]
        detected_language = translation["detectedLanguageCode"]
        await update.message.reply_text(
            f"{config.LANGUAGE_CODES_TO_FLAGS.get(detected_language, detected_language)}: {text}\n"
            f"{config.LANGUAGE_CODES_TO_FLAGS['ru']}: {translation_text}")
    else:
        raise ValueError(f"No such message handler {message_handler}")