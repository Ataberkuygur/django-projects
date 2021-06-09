from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/', default='avatar/default.png')
    friends = models.ManyToManyField('self', related_name='friends', blank=True)
    score = models.PositiveIntegerField(default=0)
    goal_score = models.PositiveIntegerField(default=0)
    daily_score = models.PositiveIntegerField(default=0)
    last_login = models.DateTimeField(null=True, auto_now=True)

    def get_friends_count(self):
        friends_count = self.friends.count()
        print(friends_count)
        return friends_count

    def get_day_score(self):
        total_score = 0
        for task in self.task_set.all():
            total_score += task.score  
        try:
            print(self.daily_score)
            self.daily_score = int(total_score) / int(self.goal_score * 10)
            self.daily_score = int(self.daily_score * 100)
            self.save()
        except:
            self.daily_score = 1
        return self.daily_score

    
    def __str__(self):
        return '%s' % (self.username)

    def save(self ,*args ,**kwargs):
        return super(CustomUser, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    def get_logout_url(self):
        return reverse('User:logout')

    def get_custom_user_settings(self):
        return reverse('User:settings', kwargs={'slug': self.slug})

    def get_absolute_url(self):
        return reverse('User:profile', kwargs={'slug': self.slug})

    def get_unique_slug(self):
        number = 0
        original_slug = '%s' % (self.user.username.replace('ı','i'))
        unique_slug = slugify(original_slug)
        while Profile.objects.filter(slug = original_slug).exists():
            number += 1
            unique_slug = '%s %d' % (original_slug, number)
            unique_slug = slugify(unique_slug)
        return unique_slug

    def __str__(self):
        return "%s's Profile" % (self.user.username)
    
    def save(self, *args , **kwargs):
        self.slug = self.get_unique_slug()
        return super(Profile, self).save(*args, **kwargs)

@receiver(post_save, sender=CustomUser)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
post_save.connect(post_save_create_profile, sender=CustomUser)    




