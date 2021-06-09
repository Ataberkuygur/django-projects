from django.db.models.fields import related
from User.models import CustomUser
from django.db import models
from django.utils.text import slugify
from django.shortcuts import reverse

class Group(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, editable=False)
    description = models.CharField(max_length=300, null=True, blank=True)
    members = models.ManyToManyField(CustomUser, related_name='members')
    created_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('Group:detail', kwargs={"slug": self.slug})

    def get_unique_slug(self):
        number = 0
        original_slug = '%s' % (self.name.replace('ı','i'))
        unique_slug = slugify(original_slug)
        while Group.objects.filter(slug = original_slug).exists():
            number += 1
            unique_slug = '%s %d' % (original_slug, number)
            unique_slug = slugify(unique_slug)
        return unique_slug


    def __str__(self):
        return '%s' % self.name
    
    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        return super(Group, self).save(*args, **kwargs)