import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

import config


def menu(mode: str, language: str=""):
    #todo: add emojis to buttons

    mode = "text_translations"
    language_flag = config.LANGUAGE_UNICODE_FLAGS.get(language, "")

    if mode == "text_translations":
        mode_buttons = [
                [InlineKeyboardButton("start study session", callback_data="text_translations|start")],
                [InlineKeyboardButton("add questions", callback_data="text_translations|add_questions")],
                [InlineKeyboardButton("statistics", callback_data="text_translations|statistics")],
            ]
    else:
        mode_buttons = []

    keyboard = [
            [InlineKeyboardButton(f"{language_flag} language", callback_data="set_language_to_study|")],  #todo: add current language flag
            [InlineKeyboardButton("mode", callback_data="set_mode|")], #todo: add current mode in button text
        ]\
        + mode_buttons\
        + [
            [
                InlineKeyboardButton("settings", callback_data="settings"),
                InlineKeyboardButton("help", callback_data="help"),
            ],
        ]
    return "Menu:", InlineKeyboardMarkup(keyboard)


def set_language_to_study():
    keyboard = [[InlineKeyboardButton(f"{config.LANGUAGE_UNICODE_FLAGS.get(lang, '')} {lang}", callback_data=f"set_language_to_study|{lang}")]
                    for lang in config.LANGUAGES]
    return "Choose language to study:", InlineKeyboardMarkup(keyboard)


def back_to_menu(text):
    #todo: maybe remove this confirmation
    keyboard = [[InlineKeyboardButton("back to menu", callback_data="menu")]]
    return text, InlineKeyboardMarkup(keyboard)

def modes():
    keyboard = [[InlineKeyboardButton("text translations", callback_data="set_mode|text_translations")]]
    return "Choose studying mode:", InlineKeyboardMarkup(keyboard)
