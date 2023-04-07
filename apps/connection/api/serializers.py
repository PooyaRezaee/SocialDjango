from rest_framework import serializers
from apps.accounts.models import User

class FollowUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'profile_picture', 'private_account')