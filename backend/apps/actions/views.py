from rest_framework import views, permissions, status
from rest_framework.response import Response
from django.utils.translation import gettext as _

from api.v1.permissions import IsOwner
from .serializers import StartInvitingSerializer, \
    StartMessagingSerializer, StartScrappingSerializer
from .tasks import invites_task, messages_task, scrape_task


class StartInvitingView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = StartInvitingSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            if request.user.balance < 0:
                return Response({'status': _('Please, refill your balance '
                                             'to start inviting.')},
                                status=status.HTTP_403_FORBIDDEN)
            t = invites_task.delay(
                limit=serializer.data['limit'],
                user_id=request.user.pk,
                source_group_id=serializer.data['source_group_id'],
                target_group_id=serializer.data['target_group_id'],
                # numbers_list=serializer.data.get('user_numbers_list'),
                use_system_numbers=serializer.data['use_system_numbers']
            )
            return Response({'status': _('Process started.'),
                             'task_id': t.task_id})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class StartMessagingView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = StartMessagingSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            if request.user.balance < 0:
                return Response({'status': _('Please, refill your balance '
                                             'to start inviting.')},
                                status=status.HTTP_403_FORBIDDEN)
            t = messages_task.delay(
                limit=serializer.data['limit'],
                user_id=request.user.pk,
                group_id=serializer.data['group_id'],
                message_id=serializer.data['message_id'],
                # numbers_list=serializer.data.get('user_numbers_list'),
                use_system_numbers=serializer.data['use_system_numbers']
            )
            return Response({'status': _('Process started.'),
                             'task_id': t.task_id})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class StartScrappingView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = StartScrappingSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            t = scrape_task.delay(
                user_id=request.user.pk,
                group_id=serializer.data['group_id'],
                tg_account_id=serializer.data.get('telegram_account_id'),
            )
            return Response({'status': _('Process started.'),
                             'task_id': t.task_id})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
