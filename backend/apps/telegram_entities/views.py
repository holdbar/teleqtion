import uuid

from django.db.models import Q
from rest_framework import viewsets, permissions, mixins

from api.v1.permissions import IsOwner
from api.v1.pagination import SmallResultsSetPagination, StandardResultsSetPagination

from .models import TelegramContact, TelegramGroup, Message
from .serializers import TelegramGroupSerializer,\
    TelegramContactSerializer, MessageSerializer


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
    pagination_class = StandardResultsSetPagination

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
                pass

        return queryset


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    pagination_class = StandardResultsSetPagination

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
