from rest_framework import serializers
from apps.accounts.models import User
from dj_rest_auth.registration.serializers import RegisterSerializer


class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def get_cleaned_data(self):
        super().get_cleaned_data()
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
        }


class ProfileImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('profile_picture',)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','age','first_name','last_name','bio','private_account')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['count_followers'] = instance.followers_real.count()
        ret['count_followings'] = instance.followings_real.count()

        return ret
