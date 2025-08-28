from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Unread first, then newest first
        notifications = Notification.objects.filter(recipient=request.user).order_by("is_read", "-timestamp")
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
