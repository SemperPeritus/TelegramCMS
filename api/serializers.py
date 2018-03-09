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

    def create(self, validated_data):
        return Bot.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.token = validated_data.get('token', instance.token)
        instance.save()
        return instance


class ChannelSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.ReadOnlyField(source='channel.title')
    username = serializers.ReadOnlyField(source='channel.username')
    bot = serializers.ReadOnlyField(source='channel.bot')

    class Meta:
        model = Channel
        fields = ('title', 'username', 'bot')


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
