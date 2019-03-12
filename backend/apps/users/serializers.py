from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from rest_auth.serializers import UserDetailsSerializer, LoginSerializer
from rest_auth.registration.serializers import RegisterSerializer

UserModel = get_user_model()


class CustomLoginSerializer(LoginSerializer):
    username = None


class CustomUserDetailsSerializer(UserDetailsSerializer):
    balance = serializers.DecimalField(max_digits=40, decimal_places=2,
                                       coerce_to_string=False, read_only=True)

    class Meta:
        model = UserModel
        fields = ('email', 'balance')
        read_only_fields = ('email', 'balance')


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    password1 = None
    password2 = None

    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        return data

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password', ''),
            'email': self.validated_data.get('email', ''),
        }
