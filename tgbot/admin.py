from django.contrib import admin

from .models import User, UserActionLog, BugReport


admin.site.register(User)
admin.site.register(UserActionLog)
admin.site.register(BugReport)
