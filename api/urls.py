from django.urls import path, include
from rest_framework import routers, viewsets, serializers

from bots.models import Message, Channel, Bot


class BotSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bot
        fields = ('name', 'username')


class BotViewSet(viewsets.ModelViewSet):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer


class ChannelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Channel
        fields = ('title', 'username', 'bot')


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


class MessageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, max_length=None, allow_empty_file=True, use_url=True)

    class Meta:
        model = Message
        fields = ('id', 'channel', 'text', 'image', 'send_time')


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


router = routers.DefaultRouter()
router.register(r'bots', BotViewSet)
router.register(r'channels', ChannelViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]
