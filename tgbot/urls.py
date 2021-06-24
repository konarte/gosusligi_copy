from django.urls import path

from . import views

urlpatterns = [
    # TODO: replace this with something more secure
    path('telegram_webhook_thing', views.TelegramBotWebhookView.as_view(), name='index'),
]

