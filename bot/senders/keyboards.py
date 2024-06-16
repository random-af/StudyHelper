import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes


def menu():
    #todo: add emojis to buttons

    mode_buttons = []

    keyboard = [
            [InlineKeyboardButton("language", callback_data="set_language_to_study|")],  #todo: add current language flag

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
    keyboard = [
            [InlineKeyboardButton("english", callback_data="set_language_to_study|english")],

            [InlineKeyboardButton("spanish", callback_data="set_language_to_study|spanish")],
        ]
    return "Choose language to study:", InlineKeyboardMarkup(keyboard)


def back_to_menu(text):
    keyboard = [[InlineKeyboardButton("back to menu", callback_data="menu")]]
    return text, InlineKeyboardMarkup(keyboard)

def modes():
    keyboard = [[InlineKeyboardButton("text translations", callback_data="set_mode|text_translations")]]
    return "Choose studying mode:", InlineKeyboardMarkup(keyboard)
