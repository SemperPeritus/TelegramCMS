from django.contrib.auth.models import User
from rest_framework import serializers

from bots.models import Bot, Channel, Message


class UserSerializer(serializers.ModelSerializer):
    bots = serializers.PrimaryKeyRelatedField(many=True, queryset=Bot.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'bots')


class BotSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ('id', 'bot_id', 'name', 'username')


class BotSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ('token',)


class ChannelSerializer(serializers.ModelSerializer):
    channel_id = serializers.ReadOnlyField()
    title = serializers.ReadOnlyField()

    class Meta:
        model = Channel
        fields = ('id', 'channel_id', 'title', 'username', 'bot')


class MessageSerializer(serializers.ModelSerializer):
    channel_title = serializers.ReadOnlyField(source='channel.title')
    image = serializers.ImageField(write_only=True, required=False)
    image_url = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Message
        fields = ('id', 'channel', 'channel_title', 'text', 'image', 'image_url', 'send_time', 'owner')

    @staticmethod
    def get_image_url(obj):
        if obj.image:
            return obj.image.url
        else:
            return None
