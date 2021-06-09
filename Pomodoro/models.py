from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from User.models import CustomUser

class Pomodoro(models.Model):
    title = models.CharField(max_length=100, default='Pomodoro Time')
    minutes = models.PositiveIntegerField(default=25)
    seconds = models.PositiveIntegerField(default=00)
    rest_minutes = models.PositiveIntegerField(default=5)
    rest_seconds = models.PositiveIntegerField(default=00)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.title)

    def save(self, *args, **kwargs):
        if (type(self.seconds) != int):
            self.seconds = 00
        if (type(self.rest_seconds) != int):
            self.rest_seconds = 00
        if (len(self.title) < 1):
            self.title = 'Pomodoro'
        return super(Pomodoro, self).save(*args, **kwargs)
