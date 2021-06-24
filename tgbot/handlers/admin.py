import datetime

import telegram
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
