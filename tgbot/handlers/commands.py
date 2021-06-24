import os
import random

from pyqrcode import QRCode
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from main.models import PageInfo

from gosusligi_copy import settings

from tgbot.handlers.static_text import *
from tgbot.handlers.utils import extract_user_data_from_update
from tgbot.ihatethis import handler_logging
from tgbot.models import User


@handler_logging
def start_command(update, context):
    u, created = User.get_user_and_created(update, context)

    # TODO: use static_text.py
    if created:
        text = NEW_USER_START_COMMAND
        # text = static_text.start_created.format(first_name=u.first_name)
    else:
        text = OLD_USER_START_COMMAND
        # text = static_text.start_not_created.format(first_name=u.first_name)
    # TODO: has a keyboard with a button that says "lets go" or smthing
    update.message.reply_text(text=text, reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton(START_COMMAND_BUTTON, callback_data=f'ok_lets_start')
    ]]))


@handler_logging
def okay_lets_start(update: Update, context: CallbackContext):
    update.callback_query.answer()
    u = User.objects.filter(user_id=extract_user_data_from_update(update)['user_id']).first()
    text_to_send = PLEASE_SEND_NAME
    context.dispatcher.bot.send_message(chat_id=extract_user_data_from_update(update)['user_id'],
                                        text=text_to_send)
    PageInfo.objects.create(creator=u)
    return 0


@handler_logging
def name(update: Update, context):
    u = User.objects.filter(user_id=update.message.from_user.id).first()
    text_to_send = PLEASE_SEND_DATE_OF_BIRTH
    context.dispatcher.bot.send_message(chat_id=extract_user_data_from_update(update)['user_id'],
                                        text=text_to_send)
    pi = PageInfo.objects.filter(creator=u).order_by('creation_date').last()
    pi.name = update.message.text
    pi.save()
    return 1


@handler_logging
def date_of_birth(update, context):
    u = User.objects.filter(user_id=update.message.from_user.id).first()
    text_to_send = PLEASE_SEND_FIRST_2_DIGITS
    context.dispatcher.bot.send_message(chat_id=extract_user_data_from_update(update)['user_id'], text=text_to_send)
    pi = PageInfo.objects.filter(creator=u).order_by('creation_date').last()
    pi.date_of_birth = update.message.text
    pi.save()
    return 2


@handler_logging
def passport_2_digits(update, context):
    u = User.objects.filter(user_id=update.message.from_user.id).first()
    text_to_send = PLEASE_SEND_LAST_3_DIGITS
    context.dispatcher.bot.send_message(chat_id=extract_user_data_from_update(update)['user_id'],
                                        text=text_to_send)
    pi = PageInfo.objects.filter(creator=u).order_by('creation_date').last()
    pi.first_two_passport_numbers = update.message.text
    pi.save()
    return 3


@handler_logging
def passport_3_digits(update, context):
    u = User.objects.filter(user_id=update.message.from_user.id).first()
    pi = PageInfo.objects.filter(creator=u).order_by('creation_date').last()
    text_to_send = CONFIRMATION_TEXT.format(
        name=pi.name,
        date_of_birth=pi.date_of_birth,
        first_two_passport_numbers=pi.first_two_passport_numbers,
        last_three_passport_numbers=update.message.text
    )
    context.dispatcher.bot.send_message(chat_id=extract_user_data_from_update(update)['user_id'],
                                        text=text_to_send, reply_markup=
                                        InlineKeyboardMarkup([[
                                            InlineKeyboardButton(YES_CONFIRMATION_BUTTON,
                                                                 callback_data=f'okay'),
                                            InlineKeyboardButton(NO_CONFIRMATION_BUTTON,
                                                                 callback_data=f'cancel'),
                                        ]]))
    pi.last_three_passport_numbers = update.message.text
    pi.save()
    return 4


@handler_logging
def cancel(update: Update, context):
    update.callback_query.answer()
    u = User.objects.filter(user_id=extract_user_data_from_update(update)['user_id']).first()
    text_to_send = CANCELLING_TEXT
    context.dispatcher.bot.send_message(chat_id=extract_user_data_from_update(update)['user_id'],
                                        text=text_to_send)
    PageInfo.objects.filter(creator=u).order_by('creation_date').last().delete()
    return ConversationHandler.END


@handler_logging
def done(update, context: CallbackContext):
    update.callback_query.answer()
    u = User.objects.filter(user_id=extract_user_data_from_update(update)['user_id']).first()
    pi = PageInfo.objects.filter(creator=u).order_by('creation_date').last()
    url = f'https://{settings.HOSTNAME}/vaccine/cert/verify/{pi.uuid}'
    qr = QRCode(url)
    qr_name = f'qrcode{random.randint(1000, 9999)}.png'
    qr.png(qr_name, scale=8)
    text_to_send = DONE_TEXT.format(url=url)
    context.dispatcher.bot.send_photo(chat_id=extract_user_data_from_update(update)['user_id'],
                                      caption=text_to_send, photo=open(qr_name, 'rb'))
    os.remove(qr_name)
    return ConversationHandler.END


@handler_logging
def help_command(update, context):
    text_to_send = HELP_MESSAGE
    context.dispatcher.bot.send_message(chat_id=extract_user_data_from_update(update)['user_id'], text=text_to_send)


@handler_logging
def contact_command(update, context):
    text_to_send = CONTACT_MESSAGE
    context.dispatcher.bot.send_message(chat_id=extract_user_data_from_update(update)['user_id'], text=text_to_send)
