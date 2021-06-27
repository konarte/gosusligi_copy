import datetime
import time

import telegram
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now

from main.models import PageInfo
from tgbot.handlers import static_text
from tgbot.ihatethis import handler_logging
from tgbot.models import User


@handler_logging
def admin(update, context):
    """ Show help info about all secret admins commands """
    u = User.get_user(update, context)
    if not u.is_admin:
        return

    return update.message.reply_text(static_text.secret_admin_commands)


@handler_logging
def invite_command(update, context):
    admin_u = User.get_user(update, context)
    if not admin_u.is_admin:
        return
    if len(update.message.text.split("@")) == 1:
        update.message.reply_text("bruh, use /invite <username> (@durov or smthing)")
        return
    username = update.message.text.split("@")[1]
    try:
        u = User.objects.get(username=username)
        u.is_invited = True
        u.save()
        context.dispatcher.bot.send_message(
            chat_id=u.user_id,
            text="тебе кинул инвайт админ!! теперь ты можешь пользоваться ботом как нормальный человек"
        )
        update.message.reply_text(f"done, @{username} is invited")
    except ObjectDoesNotExist:
        update.message.reply_text(f"seems like @{username} never messaged the bot. not invited.")


@handler_logging
def bot_stats(update, context):
    u = User.get_user(update, context)
    if not u.is_admin:
        return

    text = f"""
*Пользователи*: {User.objects.count()}
*Активные в последние 24 часа*: {User.objects.filter(updated_at__gte=now() - datetime.timedelta(hours=24)).count()}
    """
    return update.message.reply_text(
        text,
        parse_mode=telegram.ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )


@handler_logging
def site_stats(update, context):
    u = User.get_user(update, context)
    if not u.is_admin:
        return

    text = f"""
*Кол-во фейк вакцинаций*: {PageInfo.objects.count() - PageInfo.objects.filter(last_three_passport_numbers='').count()}
*Кол-во новых фейк вакцинаций за последние 24 часа*: {PageInfo.objects.filter().filter(
        updated_at__gte=now() - datetime.timedelta(hours=24)).count() - 
                                                      PageInfo.objects.filter(
        updated_at__gte=now() - datetime.timedelta(hours=24)).filter(last_three_passport_numbers='').count()}
    """
    return update.message.reply_text(
        text,
        parse_mode=telegram.ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )


@handler_logging
def broadcast_command(update, context):
    u = User.get_user(update, context)
    if not u.is_admin:
        return
    broadcast_message = update.message.text.split("/broadcast ")[1]
    yep = User.objects.all()
    counter = 0
    for user_id in [i.user_id for i in yep]:
        try:
            context.dispatcher.bot.send_message(chat_id=user_id, text=broadcast_message)
            counter += 1
            if counter % 25 == 0:
                update.message.reply_text(f"sent {counter} messages so far!")
        except Exception as e:
            print(e)
        time.sleep(0.45)
    update.message.reply_text(f"done, {counter} messages sent out total.")
