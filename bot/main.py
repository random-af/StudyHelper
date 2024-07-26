from telegram.ext import Application, CallbackQueryHandler, CommandHandler , ContextTypes, MessageHandler

import handlers.buttons as buttons
import handlers.commands as commands
import handlers.messages as messages


def main():
    application = Application.builder().token("").build()

    application.add_handler(CommandHandler("menu", commands.menu))
    application.add_handler(CallbackQueryHandler(buttons.set_language_to_study, pattern="^set_language_to_study"))
    application.add_handler(CallbackQueryHandler(buttons.modes, pattern="^set_mode"))
    application.add_handler(CallbackQueryHandler(buttons.menu, pattern="^menu"))
    application.add_handler(MessageHandler(callback=messages.handle_message, filters=None))

    print('run')
    application.run_polling()


if __name__ == '__main__':
    main()
