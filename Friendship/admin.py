from Friendship.models import Friendship
from django.contrib import admin

class FriendshipAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'following_date']

    class Meta:
        model = Friendship

admin.site.register(Friendship, FriendshipAdmin)