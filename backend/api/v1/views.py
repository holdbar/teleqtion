from django.utils.translation import gettext as _
from rest_framework.views import APIView
from rest_framework.response import Response
from celery.result import AsyncResult


class GetTaskStatusView(APIView):
    def get(self, request, task_id):
        result = AsyncResult(task_id)
        if result.ready():
            return Response(result.result)
        else:
            return Response({'status': _('Task is still in progress.')})
