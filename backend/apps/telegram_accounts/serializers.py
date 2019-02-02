from rest_framework import serializers

from .models import TelegramAccount


class TelegramAccountSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = TelegramAccount
        exclude = ('phone_code_hash', 'session', 'api_id', 'api_hash')


class TelegramAccountConfirmSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    code = serializers.IntegerField()


class TelegramAccountCodeRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
