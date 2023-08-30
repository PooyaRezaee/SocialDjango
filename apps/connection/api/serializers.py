from rest_framework import serializers
from apps.accounts.models import User

class FollowUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'profile_picture', 'private_account')

    # def to_representation(self, instance): # NOTE if send request in context Automat return full like url with base
    #     representation = super().to_representation(instance)
    #     representation['profile_picture'] = self.context['request'].build_absolute_uri(representation['profile_picture'])
    #
    #     return representation
