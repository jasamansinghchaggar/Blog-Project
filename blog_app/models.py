from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()


    def get_absolute_url(self):
        return reverse('blog_app:post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey('blog_app.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)
    create_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def date(self):
        self.create_date = timezone.now()
        self.save()

    def approve(self):
        self.approved_comment = True
        self.save()


    def get_absolute_url(self):
        return reverse('post_list')
    
    def __str__(self):
        return self.text[:10]