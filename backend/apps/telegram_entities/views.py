import uuid

from django.db.models import Q
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from api.v1.permissions import IsOwner
from api.v1.pagination import SmallResultsSetPagination
from apps.actions.models import InviteEvent, MessageEvent

from .models import TelegramContact, TelegramGroup, Message
from .serializers import TelegramGroupSerializer, \
    TelegramContactSerializer, MessageSerializer, \
    TelegramContactListSerializer, TelegramContactByGroupSerializer, \
    TelegramContactsNotInvitedSerializer, NotMessagedSerializer


class TelegramGroupViewSet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    serializer_class = TelegramGroupSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    pagination_class = SmallResultsSetPagination

    def get_queryset(self):
        queryset = TelegramGroup.objects.filter(
            user=self.request.user
        ).order_by('-added_at')
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) | Q(title__icontains=search)
            )
        return queryset


class TelegramContactViewSet(mixins.ListModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    serializer_class = TelegramContactSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    pagination_class = SmallResultsSetPagination

    def get_queryset(self):
        queryset = TelegramContact.objects.filter(
            user=self.request.user
        ).order_by('priority', '-added_at')
        username = self.request.query_params.get('username')
        group = self.request.query_params.get('group')

        if username:
            queryset = queryset.filter(
                username__icontains=username
            )

        if group:
            try:
                uuid.UUID(group)
                queryset = queryset.filter(
                    group__id=group
                )
            except ValueError:
                queryset = list()

        return queryset

    @action(detail=False, methods=['post'],
            serializer_class=TelegramContactListSerializer,
            url_path='delete-list')
    def delete_list(self, request):
        serializer = TelegramContactListSerializer(data=request.data,
                                                   context={'request': request})
        if serializer.is_valid():
            TelegramContact.objects.filter(id__in=serializer.data['id_list']).delete()
            return Response(status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'],
            serializer_class=TelegramContactByGroupSerializer,
            url_path='delete-all')
    def delete_all(self, request):
        serializer = TelegramContactByGroupSerializer(data=request.data,
                                                      context={'request': request})
        if serializer.is_valid():
            TelegramContact.objects.filter(group__id=serializer.data['group_id']).delete()
            return Response(status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'],
            serializer_class=TelegramContactsNotInvitedSerializer,
            url_path='get-not-invited-count')
    def get_not_invited_count(self, request):
        serializer = TelegramContactsNotInvitedSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            all_contacts = TelegramContact.objects.filter(
                group__id=serializer.data['source_group_id']
            )
            invites = InviteEvent.objects.filter(
                source_group__id=serializer.data['source_group_id'],
                target_group__id=serializer.data['target_group_id'],
                user=request.user
            )
            processed_contacts = [i.contact for i in invites]
            not_processed_contacts = [i for i in all_contacts
                                      if i not in processed_contacts]
            return Response(
                {'count': len(not_processed_contacts)},
                status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'],
            serializer_class=NotMessagedSerializer,
            url_path='get-not-messaged-count')
    def get_not_messaged_count(self, request):
        serializer = NotMessagedSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            all_contacts = TelegramContact.objects.filter(
                group__id=serializer.data['group_id']
            )
            messages = MessageEvent.objects.filter(
                telegram_group__id=serializer.data['group_id'],
                message__id=serializer.data['message_id'],
                user=request.user
            )
            processed_contacts = [i.contact for i in messages]
            not_processed_contacts = [i for i in all_contacts
                                      if i not in processed_contacts]
            return Response(
                {'count': len(not_processed_contacts)},
                status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    pagination_class = SmallResultsSetPagination

    @staticmethod
    def clean_message_text(text):
        for_remove = (
            ('<p>', ''),
            ('</p>', ''),
            ('<br>', '\n'),
            ('&amp;', '&'),
            ('&lt;', '<'),
            ('&gt;', '>'),
            ('&quot;', '"'),
            ('&#39;', "'"),
            (' target="_blank"', ''),
            ('<blockquote>', '<code>'),
            ('</blockquote>', '</code>'),
            (' class="ql-syntax" spellcheck="false"', ''),
        )
        for i in for_remove:
            text = text.replace(i[0], i[1])
        return text

    def get_queryset(self):
        queryset = Message.objects.filter(
            user=self.request.user
        ).order_by('-added_at')
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                title__icontains=search
            )
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            request.data['text'] = self.clean_message_text(request.data['text'])
        return super(MessageViewSet, self).create(request, *args, **kwargs)
