from django.db import models
from apps.accounts.models import User
from taggit.managers import TaggableManager

class PublicPostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(author__private_account=False)

class Post(models.Model):
    title = models.CharField(max_length=64)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='posts')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    tags = TaggableManager()

    def __str__(self):
        return self.title

    objects = models.Manager() # default manager
    public_posts = PublicPostManager()



class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='likes')

    def __str__(self):
        return str(self.user)
        