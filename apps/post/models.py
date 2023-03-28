from django.db import models
from apps.accounts.models import User
from taggit.managers import TaggableManager

class Post(models.Model):
    title = models.CharField(max_length=64)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    tags = TaggableManager()

    def __str__(self):
        return self.title



class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.user


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    replied_to = models.ForeignKey('self', on_delete=models.SET_NULL,blank=True,null=True)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creataed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
    