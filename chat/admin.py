from django.contrib import admin
from . import models


admin.site.register(models.ChatGroup)
admin.site.register(models.ChatMessage)
