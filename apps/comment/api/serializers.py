from rest_framework import serializers
from django.utils.timesince import timesince
from datetime import datetime
from apps.post.api.serializers import AuthorSerializer
from apps.comment.models import Comment

class CreateCommentSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=512)
    comment_id = serializers.IntegerField(required=False, default=None)

    def validate_comment_id(self, value):
        if value is not None and not Comment.objects.filter(id=value).exists():
            raise serializers.ValidationError("Comment with this id does not exist.")
        return value

class CommentSerializer(serializers.ModelSerializer):
    user = AuthorSerializer()

    class Meta:
        model = Comment
        exclude = ('replied_to','post')

    def get_humanize_time(self, time):
        time = time.split('.')[0]
        try:
            return timesince(datetime.strptime(time, "%Y-%m-%d %H:%M:%S"))
        except ValueError:
            return timesince(datetime.strptime(time, "%Y-%m-%dT%H:%M:%S"))


    def to_representation(self, instance):
        ret = super().to_representation(instance)

        have_reply = instance.reply.exists()
        ret['created'] = self.get_humanize_time(str(ret['created']))
        ret['have_reply'] = have_reply
        return ret