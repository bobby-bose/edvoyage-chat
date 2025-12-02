from django.contrib import admin
from .models import UserSimple, Conversation, Message

admin.site.register(UserSimple)
admin.site.register(Conversation)
admin.site.register(Message)
