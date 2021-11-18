from telegram import Bot

from stabibot import settings

bot = Bot(token=settings.TELEGRAM_AUTH_TOKEN)


def send_message(message: str):
    bot.send_message(settings.TELEGRAM_CHAT_ID, message)
