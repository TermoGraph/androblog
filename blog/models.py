from django.db import models
from django.conf import settings

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=300, db_index=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='posts/')
    body = models.TextField(db_index=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date']

class App(models.Model):
    app_type = models.CharField(max_length=100, db_index=True, blank=True)
    title = models.CharField(max_length=300, db_index=True)
    body = models.TextField(db_index=True)
    image = models.ImageField(upload_to='apps/')
    file = models.FileField(upload_to='mods/', blank=True)
    pub_date = models.DateTimeField()
    url = models.CharField(max_length=500, blank=True, db_index=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-pub_date']

class PublicUsers(models.Model):
    username = models.CharField(max_length=100, db_index=True)
    password1 = models.CharField(max_length=100, db_index=True)
    password2 = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.username
    
    class Meta:
        ordering = ['username']

class Comment(models.Model):
    author = models.ForeignKey(PublicUsers, on_delete=models.CASCADE)
    post_slug = models.SlugField()
    text = models.TextField(db_index=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pub_date']
