from django.utils.timesince import timesince
from datetime import datetime
from rest_framework import serializers
from apps.post.models import Post
from apps.accounts.models import User
from taggit.serializers import TagListSerializerField,TaggitSerializer

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

    def to_representation(self, instance):
        return instance.username

class PostsSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Post
        fields = '__all__'
    
    def get_humanize_time(self, time):
        time = time.split('.')[0]
        return timesince(datetime.strptime(time, "%Y-%m-%dT%H:%M:%S"))

    def get_is_modified(self, obj):
        return obj.created != obj.modified

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        ret['is_modified'] = self.get_is_modified(instance)
        ret.pop('modified')

        ret['created'] = self.get_humanize_time(ret['created'])
        return ret

class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title','text')

class PostDetailSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = '__all__'