from django.utils.timesince import timesince
from datetime import datetime
from rest_framework import serializers
from apps.post.models import Post,Like
from apps.accounts.models import User
from taggit.serializers import TagListSerializerField,TaggitSerializer

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

    def to_representation(self, instance):
        return instance.username

class PostsSerializer(TaggitSerializer,serializers.ModelSerializer):
    author = AuthorSerializer()
    tags = TagListSerializerField()

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
        ret['count_likes'] = Like.objects.filter(post=instance).count()
        return ret

class CreatePostSerializer(TaggitSerializer,serializers.ModelSerializer):
    tags = TagListSerializerField(required=False)

    class Meta:
        model = Post
        fields = ('title','text','tags')

class PostDetailSerializer(TaggitSerializer,serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('created_at','modified')
    
    def get_is_modified(self, obj):
        return obj.created != obj.modified

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        ret['is_modified'] = self.get_is_modified(instance)
        ret.pop('modified')

        ret['count_likes'] = Like.objects.filter(post=instance).count()

        return ret