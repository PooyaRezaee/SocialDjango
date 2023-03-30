from django.db import models
from apps.post.models import Post
from apps.accounts.models import User

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    replied_to = models.ForeignKey('self', on_delete=models.SET_NULL,blank=True,null=True,related_name='reply')
    text = models.CharField(max_length=512)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comments')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
    