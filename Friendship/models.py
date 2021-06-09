from django.db import models
from django.db.models.fields.related import RelatedField
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from User.models import CustomUser
import datetime

class Friendship(models.Model):
    STATUS = (
        ('send', 'send'),
        ('accepted', 'accepted'),
    )
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender', null=True)
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver', null=True)
    following_date = models.DateTimeField(editable=False, null=True)
    status = models.CharField(max_length=8, choices=STATUS)

    def __str__(self):
        return '%s - %s Friendship' % (self.sender, self.receiver)

    def save(self, *args, **kwargs):
        if self.status == 'accepted':
            self.following_date = datetime.datetime.now()
        return super(Friendship, self).save(*args, **kwargs)

@receiver(post_save, sender=Friendship)
def post_save_add_to_friends(sender, instance, **kwargs):
    receiver_ = instance.receiver
    sender_ = instance.sender
    if instance.status == 'accepted':
        receiver_.friends.add(sender_)
        sender_.friends.add(receiver_)
        
    receiver_.save()
    sender_.save()

@receiver(pre_delete, sender=Friendship)
def pre_delete_remove_from_friend(sender, instance, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    receiver_.friends.remove(sender_)
    sender_.friends.remove(receiver_)
    receiver_.save()
    sender_.save()

post_save.connect(post_save_add_to_friends, sender=Friendship)
    