from rest_framework import serializers
from django.utils.translation import gettext as _


class StartInvitingSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    source_group_id = serializers.UUIDField()
    target_group_id = serializers.UUIDField()
    use_system_numbers = serializers.BooleanField()
    user_numbers_list = serializers.ListField()
    limit = serializers.IntegerField()

    def validate_user_numbers_list(self, value):
        if len(value) < 1:
            raise serializers.ValidationError(_('You must provide at least 1 '
                                                'phone number.'))
        return value

    def validate(self, attrs):
        if not attrs['use_system_numbers'] and \
                not attrs['user_numbers_list']:
            raise serializers.ValidationError(_('You must choose to use system '
                                                'numbers or your numbers.'))
        return attrs


class StartMessagingSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    group_id = serializers.UUIDField()
    message_id = serializers.UUIDField()
    use_system_numbers = serializers.BooleanField()
    user_numbers_list = serializers.ListField()
    limit = serializers.IntegerField()

    def validate_user_numbers_list(self, value):
        if len(value) < 1:
            raise serializers.ValidationError(_('You must provide at least 1 '
                                                'phone number.'))
        return value

    def validate(self, attrs):
        if not attrs['use_system_numbers'] and \
                not attrs['user_numbers_list']:
            raise serializers.ValidationError(_('You must choose to use system '
                                                'numbers or your numbers.'))
        return attrs


class StartScrappingSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    group_id = serializers.UUIDField()
    telegram_account_id = serializers.UUIDField(required=False)
