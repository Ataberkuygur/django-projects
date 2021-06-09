from django.db import models
from django.http.response import HttpResponse, JsonResponse
from User.models import CustomUser
from django.urls import reverse
from django.utils.text import slugify
import datetime 

class Category(models.Model):
    PRIORITY_CHOICES = (
        ('None', '-'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    )
    title = models.CharField(max_length=100)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='gray')
    slug = models.SlugField(unique=True, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def get_delete_url(self):
        return reverse('User:category_delete')

    def get_unique_slug(self):
        number = 0
        original_slug = '%s %s' % (self.title.replace('ı', 'i'), (self.user.username.replace('ı','i')))
        unique_slug = slugify(original_slug)
        while Category.objects.filter(slug = unique_slug).exists():
            number += 1
            unique_slug = '%s %d' % (original_slug, number)
            unique_slug = slugify(unique_slug)
        return unique_slug

    def __str__(self):
        return '%s' % self.title

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        return super(Category, self).save(*args, **kwargs)

class Task(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    done = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default = 0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category', null=True, blank=True)    
    message = models.TextField(editable=False)
    created_time = models.DateTimeField(null=True, blank=True)
    updated_time = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    def get_unique_slug(self):
        number = 0
        original_slug = '%s' % (self.title.replace('ı', 'i'))
        unique_slug = slugify(original_slug)
        while Task.objects.filter(slug = unique_slug).exists():
            number += 1
            unique_slug = '%s %d' % (original_slug, number)
            unique_slug = slugify(unique_slug)
        return unique_slug

    def done_or_not(self):
        return reverse('Task:done_or_not', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('Task:delete', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = self.get_unique_slug()
            self.created_time = datetime.datetime.now()
            self.updated_time = datetime.datetime.now()
        else:
            self.updated_time = datetime.datetime.now()
        if self.done == True:
            if self.category:
                if self.category.priority == '1':
                    self.score = 10
                elif self.category.priority == '2':
                    self.score = 10
                elif self.category.priority == '3':
                    self.score = 10
                else:
                    self.score = 10
            else:
                self.score = 10
        else:
            self.score = 0
        return super(Task, self).save(*args, **kwargs)  
