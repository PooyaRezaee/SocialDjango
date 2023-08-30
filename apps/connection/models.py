from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError


class Follow(models.Model):
    following = models.ForeignKey('accounts.User',on_delete=models.CASCADE,related_name='followings')  # user Do operation
    follower = models.ForeignKey('accounts.User',on_delete=models.CASCADE,related_name='followers')  # user followed
    timestamp = models.DateTimeField(auto_now_add=True)
    in_request = models.BooleanField()


@receiver(pre_save, sender=Follow)
def check_following_and_follower(sender, instance, **kwargs):
    if instance.following == instance.follower:
        raise ValidationError("Following and follower can't be the same user.")
    if not instance.pk and Follow.objects.filter(following=instance.following, follower=instance.follower).exists():
        raise IntegrityError("This follow relationship already exists.")
