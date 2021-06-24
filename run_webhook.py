import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gosusligi_copy.settings')
django.setup()
# it's this way because run_pooling causes some imports which require the User model, so we can't really \
# just change it since for the model to work we need django.setup() which needs the line above it
from tgbot.handlers.dispatcher import run_webhook

if __name__ == "__main__":
    run_webhook()
