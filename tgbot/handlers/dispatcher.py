from django.utils import timezone

from gosusligi_copy import settings

import telegram
from telegram.ext import (
    Updater, Dispatcher, Filters,
    CommandHandler, MessageHandler,
    CallbackQueryHandler, ConversationHandler,
)


from gosusligi_copy.settings import TELEGRAM_TOKEN, ENABLE_DECORATOR_LOGGING
from . import admin
from tgbot.handlers import commands
from ..models import UserActionLog, User


def setup_dispatcher(dp):
    """
    Adding handlers for events from Telegram
    """

    dp.add_handler(CommandHandler("start", commands.start_command))
    dp.add_handler(CommandHandler("help", commands.help_command))
    dp.add_handler(CommandHandler("contact", commands.contact_command))

    # admin commands
    dp.add_handler(CommandHandler("admin", admin.admin))
    dp.add_handler(CommandHandler("bot_stats", admin.bot_stats))
    dp.add_handler(CommandHandler("site_stats", admin.site_stats))

    # noinspection PyTypeChecker
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(commands.okay_lets_start, pattern='^ok_lets_start$')],
        states={
            # TODO: add a fallback or something so that if you mess up the regex it doesnt ignore ya
            0: [MessageHandler(Filters.regex('^(([^\\s\\d]{1,20}\\s){2}[^\\s\\d]{1,20})$'), commands.name)],
            1: [MessageHandler(Filters.regex('^([\\d]{2}\\.){2}[\\d]{4}$'), commands.date_of_birth)],
            # TODO: add a check for your date of birth, if it's less then 18 - put a warning out.
            2: [MessageHandler(Filters.regex('^[\\d]{2}$'), commands.passport_2_digits)],
            3: [MessageHandler(Filters.regex('^[\\d]{3}$'), commands.passport_3_digits)],
            # TODO: this pattern should be a constant in some file
            4: [CallbackQueryHandler(commands.done, pattern='^okay$'),
                CallbackQueryHandler(commands.cancel, pattern='^cancel$'),
                MessageHandler(Filters.all, commands.done)]
        },
        fallbacks=[CommandHandler('cancel', commands.cancel)],
    )
    dp.add_handler(conv_handler)

    return dp


def run_webhook():
    """ Run bot in webhook mode """
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = telegram.Bot(TELEGRAM_TOKEN).get_me()
    bot_link = f"https://t.me/{bot_info['username']}"

    print(f"hooking of '{bot_link}' started")
    # TODO: why is port 8000 there? it might die because of it
    updater.start_webhook(listen='0.0.0.0', port=80, url_path='tgbot/telegram_webhook_thing',
                          webhook_url=f'https://{settings.HOSTNAME}/tgbot/telegram_webhook_thing')
    updater.idle()


def run_pooling():
    """ Run bot in pooling mode """
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = telegram.Bot(TELEGRAM_TOKEN).get_me()
    bot_link = f"https://t.me/" + bot_info["username"]

    print(f"Pooling of '{bot_link}' started")
    updater.start_polling()
    updater.idle()


def process_telegram_event(update_json):
    update = telegram.Update.de_json(update_json, bot)
    dispatcher.process_update(update)


# Global variable - best way I found to init Telegram bot
bot = telegram.Bot(TELEGRAM_TOKEN)
dispatcher = setup_dispatcher(Dispatcher(bot, None, workers=0, use_context=True))
TELEGRAM_BOT_USERNAME = bot.get_me()["username"]
