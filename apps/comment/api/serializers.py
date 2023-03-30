from rest_framework import serializers
from django.utils.timesince import timesince
from datetime import datetime
from apps.post.api.serializers import AuthorSerializer
from apps.comment.models import Comment

class CreateCommentSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=512)
    comment_id = serializers.IntegerField(required=False)

class CommentSerializer(serializers.ModelSerializer):
    user = AuthorSerializer()

    class Meta:
        model = Comment
        exclude = ('replied_to','post')
    
    def get_humanize_time(self, time):
        time = time.split('.')[0]
        return timesince(datetime.strptime(time, "%Y-%m-%dT%H:%M:%S"))

    def to_representation(self, instance):    
        ret = super().to_representation(instance)

        ret['created'] = self.get_humanize_time(ret['created'])
        return ret