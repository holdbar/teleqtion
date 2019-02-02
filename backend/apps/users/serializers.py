from django.contrib.auth import get_user_model
from rest_framework import serializers

from rest_auth.serializers import UserDetailsSerializer, LoginSerializer
from rest_auth.registration.serializers import RegisterSerializer

UserModel = get_user_model()


class CustomLoginSerializer(LoginSerializer):
    username = None


class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        model = UserModel
        fields = ('pk', 'email')
        read_only_fields = ('email', )


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    password1 = None
    password2 = None

    password = serializers.CharField(write_only=True)

    def validate(self, data):
        return data

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password', ''),
            'email': self.validated_data.get('email', ''),
        }
