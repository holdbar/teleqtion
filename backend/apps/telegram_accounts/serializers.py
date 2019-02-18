from rest_framework import serializers

from .models import TelegramAccount


class TelegramAccountSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = TelegramAccount
        fields = ('id', 'user', 'phone_number', 'confirmed', 'active',
                  'error_name', 'error_datetime', 'last_used', 'added_at',
                  'invites_count', 'messages_count')


class TelegramAccountConfirmSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    code = serializers.IntegerField()


class TelegramAccountCodeRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
