from django.db import models

class Follow(models.Model):
    following = models.ForeignKey('accounts.User',on_delete=models.CASCADE,related_name='followings')  # user Do operation
    follower = models.ForeignKey('accounts.User',on_delete=models.CASCADE,related_name='followers')  # user followed
    timestamp = models.DateTimeField(auto_now_add=True)
    in_request = models.BooleanField()
