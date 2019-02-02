from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from .serializers import TelegramAccountSerializer, \
    TelegramAccountConfirmSerializer, \
    TelegramAccountCodeRequestSerializer
from .models import TelegramAccount
from .permissions import IsOwner
from .tasks import confirm_account, send_code_request


class TelegramAccountViewSet(viewsets.ModelViewSet):
    serializer_class = TelegramAccountSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return TelegramAccount.objects.filter(
            user=self.request.user
        ).order_by('-added_at')

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
