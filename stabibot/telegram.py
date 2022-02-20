import logging

from telegram import Bot
from telegram import constants

from stabibot import settings

bot = Bot(token=settings.TELEGRAM_AUTH_TOKEN)


def send_message(message: str, chat_id=settings.TELEGRAM_CHAT_ID):
    logging.info(f"Message sent to telegram:{chat_id}:")
    logging.info(message)
    bot.send_message(
        chat_id=chat_id,
        text=message,
        disable_web_page_preview=True,
        parse_mode=constants.PARSEMODE_HTML,
    )
