from django.urls import path, include
from rest_framework import routers, viewsets, serializers

from bots.models import Message, Channel, Bot


class BotSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ('id', 'name', 'username')


class BotSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ('token',)


class BotViewSet(viewsets.ModelViewSet):
    queryset = Bot.objects.all()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return BotSerializerPost
        return BotSerializerGet


class ChannelSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.ReadOnlyField(source='channel.title')
    username = serializers.ReadOnlyField(source='channel.username')
    bot = serializers.ReadOnlyField(source='channel.bot')

    class Meta:
        model = Channel
        fields = ('title', 'username', 'bot')


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


class MessageSerializer(serializers.ModelSerializer):
    channel_title = serializers.ReadOnlyField(source='channel.title')

    class Meta:
        model = Message
        fields = ('id', 'channel', 'channel_title', 'text', 'image', 'send_time')

    def create(self, validated_data):
        # message = Message(channel=validated_data.get('channel'),
        #                   text=validated_data.get('text'),
        #                   image=validated_data.get('image'),
        #                   send_time=validated_data.get('send_time'))
        # return message
        return Message(**validated_data)

    def update(self, instance, validated_data):
        instance.channel = validated_data.get('channel', instance.channel)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.send_time = validated_data.get('send_time', instance.send_time)
        return instance


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
