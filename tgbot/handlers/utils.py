from functools import wraps

from django.utils import timezone

from gosusligi_copy.settings import ENABLE_DECORATOR_LOGGING
from tgbot.models import User, UserActionLog


def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=telegram.ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func


def extract_user_data_from_update(update):
    """ python-telegram-bot's Update instance --> User info """
    if update.message is not None:
        user = update.message.from_user.to_dict()
    elif update.inline_query is not None:
        user = update.inline_query.from_user.to_dict()
    elif update.chosen_inline_result is not None:
        user = update.chosen_inline_result.from_user.to_dict()
    elif update.callback_query is not None and update.callback_query.from_user is not None:
        user = update.callback_query.from_user.to_dict()
    elif update.callback_query is not None and update.callback_query.message is not None:
        user = update.callback_query.message.chat.to_dict()
    else:
        raise Exception(f"Can't extract user data from update: {update}")

    return dict(
        user_id=user["id"],
        is_blocked_bot=False,
        **{
            k: user[k]
            for k in ["username", "first_name", "last_name", "language_code"]
            if k in user and user[k] is not None
        },
    )


def handler_logging(action_name=None):
    """ Turn on this decorator via ENABLE_DECORATOR_LOGGING variable in dtb.settings """
    def decor(func):
        def handler(update, context, *args, **kwargs):
            user, _ = User.get_user_and_created(update, context)
            action = f"{func.__module__}.{func.__name__}" if not action_name else action_name
            UserActionLog.objects.create(user_id=user.user_id, action=action, created_at=timezone.now())
            return func(update, context, *args, **kwargs)
        return handler if ENABLE_DECORATOR_LOGGING else func
    return decor
