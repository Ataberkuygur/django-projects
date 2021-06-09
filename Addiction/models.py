from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from User.models import CustomUser
import datetime

class Addiction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name =models.CharField(max_length=200)
    slug = models.SlugField(unique=True, editable=False)
    created_date = models.DateTimeField(auto_now_add=True)
    day = models.PositiveIntegerField(editable=False, null=True)
    week = models.PositiveIntegerField(editable=False, null=True)
    month = models.PositiveIntegerField(editable=False, null=True)

    def get_absolute_url(self):
        return reverse('Addiction:detail', kwargs = {'slug': self.slug})

    def get_unique_slug(self):
        number = 0
        original_slug = '%s' % (self.name.replace('ı','i'))
        unique_slug = slugify(original_slug)
        while Addiction.objects.filter(slug = original_slug).exists():
            number += 1
            unique_slug = '%s %d' % (original_slug, number)
            unique_slug = slugify(unique_slug)
        return unique_slug

    def __str__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        return super(Addiction, self).save(*args, **kwargs)