from django.contrib import admin

from .models import User, UserActionLog
# Register your models here.

admin.site.register(User)
admin.site.register(UserActionLog)
