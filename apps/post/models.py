from django.db import models
from apps.accounts.models import User
from taggit.managers import TaggableManager
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.utils import IntegrityError

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
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

@receiver(pre_save, sender=Like)
def check_like_valodation(sender, instance, **kwargs):
    if Like.objects.filter(user=instance.user, post=instance.post).exists():
        raise IntegrityError("This Like Operation already exists.")