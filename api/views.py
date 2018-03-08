from django.contrib.auth.models import User
from rest_framework import viewsets, permissions

from api.permissions import IsOwnerOrReadOnly
from api.serializers import BotSerializerPost, BotSerializerGet, ChannelSerializer, MessageSerializer, UserSerializer
from bots.models import Bot, Channel, Message


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)


class BotViewSet(viewsets.ModelViewSet):
    queryset = Bot.objects.all()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return BotSerializerPost
        return BotSerializerGet

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
