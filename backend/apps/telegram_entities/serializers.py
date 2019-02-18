from rest_framework import serializers

from .models import TelegramGroup, TelegramContact, Message


class TelegramGroupSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = TelegramGroup
        fields = ('id', 'user', 'username', 'title', 'join_link', 'added_at',
                  'updated_at', 'scrapped_count', 'invited_from_count',
                  'invited_to_count')


class TelegramContactSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = TelegramContact
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Message
        fields = '__all__'
