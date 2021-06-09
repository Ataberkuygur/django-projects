from django.db import models
from User.models import CustomUser
import uuid


class Room(models.Model):
    room_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='room_first_user', null=True)
    second_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='room_second_user', null=True)

class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user', verbose_name='Kullanıcı', null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room', verbose_name='Oda', null=True)
    content = models.TextField(verbose_name='Mesaj İçeriği')
    is_seen = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def get_short_date(self):
        created_date = str(self.created_date.hour+3) + ":" + str(self.created_date.minute)
        return created_date