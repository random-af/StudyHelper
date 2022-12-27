from telegram_bot.telegram_model import TelegramUser


def load_or_create_user(user_id, db_session):
    user = db_session.query(TelegramUser).filter(TelegramUser.id == user_id).first()
    if user is None:
        user = TelegramUser(id=user_id)
        db_session.add(user)
        db_session.commit()
    return user
