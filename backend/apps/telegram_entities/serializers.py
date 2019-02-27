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


class TelegramContactListSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    id_list = serializers.ListField()

    class Meta:
        model = TelegramContact
        fields = ('user', 'id_list')


class TelegramContactByGroupSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    group_id = serializers.UUIDField()

    class Meta:
        model = TelegramContact
        fields = ('user', 'group_id')


class TelegramContactsNotInvitedSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    source_group_id = serializers.UUIDField()
    target_group_id = serializers.UUIDField()

    class Meta:
        model = TelegramContact
        fields = ('user', 'source_group_id', 'target_group_id')


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Message
        fields = '__all__'
