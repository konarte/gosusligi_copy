import json
import logging

from django.utils import timezone
from django.views import View
from django.http import JsonResponse

from gosusligi_copy.settings import DEBUG, ENABLE_DECORATOR_LOGGING
from tgbot.handlers.dispatcher import process_telegram_event, TELEGRAM_BOT_USERNAME
from tgbot.models import User, UserActionLog

logger = logging.getLogger(__name__)

BOT_URL = f"https://t.me/{TELEGRAM_BOT_USERNAME}"


class TelegramBotWebhookView(View):
    # WARNING: if fail - Telegram webhook will be delivered again. 
    # Can be fixed with async celery task execution
    def post(self, request, *args, **kwargs):
        # TODO: add celery here
        process_telegram_event(json.loads(request.body))
        return JsonResponse({"ok": "POST request processed"})

    def get(self, request, *args, **kwargs):  # for debug
        return JsonResponse({"ok": "Get request processed. But nothing done"})




