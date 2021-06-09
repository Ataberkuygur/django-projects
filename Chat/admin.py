from Chat.models import Message
from django.contrib import admin
from .models import Room, Message

class RoomAdmin(admin.ModelAdmin):
    list_display = ['first_user', 'second_user']

    class Meta:
        model = Room

class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'created_date']

    class Meta:
        model = Message

admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)
