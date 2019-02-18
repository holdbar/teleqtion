from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.db.models import Q

from .serializers import TelegramAccountSerializer, \
    TelegramAccountConfirmSerializer, \
    TelegramAccountCodeRequestSerializer
from .models import TelegramAccount
from api.v1.permissions import IsOwner
from api.v1.pagination import SmallResultsSetPagination
from .tasks import confirm_account, send_code_request


class TelegramAccountViewSet(viewsets.ModelViewSet):
    serializer_class = TelegramAccountSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    pagination_class = SmallResultsSetPagination

    def get_queryset(self):
        queryset = TelegramAccount.objects.filter(
            user=self.request.user
        ).order_by('-added_at')
        phone_number = self.request.query_params.get('phone_number')
        active = self.request.query_params.get('active')
        confirmed = self.request.query_params.get('confirmed')
        if phone_number:
            phone_number = phone_number.strip()
            queryset = queryset.filter(
                Q(phone_number__icontains=phone_number) |
                Q(phone_number__icontains='+'+phone_number)
            )
        if active:
            queryset = queryset.filter(
                active=True if active == 't' else False
            )
        if confirmed:
            queryset = queryset.filter(
                confirmed=True if confirmed == 't' else False
            )
        return queryset

    @action(detail=False, methods=['post'],
            serializer_class=TelegramAccountCodeRequestSerializer,
            url_path='code-request')
    def code_request(self, request):
        serializer = TelegramAccountCodeRequestSerializer(data=request.data)
        if serializer.is_valid():
            account = get_object_or_404(TelegramAccount, pk=serializer.data['id'])
            if not account.confirmed:
                t = send_code_request.delay(account.id)
                return Response({'status': _('Process started.'),
                                 'task_id': t.task_id})
            else:
                return Response({'status': _('Account is already confirmed.')},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'],
            serializer_class=TelegramAccountConfirmSerializer,
            url_path='confirm')
    def confirm(self, request):
        serializer = TelegramAccountConfirmSerializer(data=request.data)
        if serializer.is_valid():
            account = get_object_or_404(TelegramAccount, pk=serializer.data['id'])
            if not account.confirmed:
                t = confirm_account.delay(account.id, serializer.data['code'])
                return Response({'status': _('Process started.'),
                                 'task_id': t.task_id})
            else:
                return Response({'status': _('Account is already confirmed.')},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
