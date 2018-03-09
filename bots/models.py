import os
from builtins import super

import telegram
from celery.result import AsyncResult
from django.db import models
from django.dispatch import receiver
from django.utils.safestring import mark_safe

from TelegramCMS import settings
from bots import tasks


class Bot(models.Model):
    bot_id = models.IntegerField()
    name = models.CharField(max_length=64)
    username = models.CharField(max_length=32)
    token = models.CharField(max_length=45)
    owner = models.ForeignKey('auth.User', related_name='bots', on_delete=models.CASCADE)

    def __str__(self):
        return "{0} (@{1})".format(self.name, self.username)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        bot = telegram.Bot(token=self.token)

        bot_info = bot.get_me()

        self.bot_id = bot_info['id']
        self.name = bot_info['first_name']
        self.username = bot_info['username']

        super().save(force_insert, force_update, using, update_fields)


class Channel(models.Model):
    channel_id = models.BigIntegerField()
    type = models.CharField(max_length=32)
    title = models.CharField(max_length=128, editable=False)
    username = models.CharField(max_length=32)
    bot = models.ForeignKey(Bot, null=True, blank=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey('auth.User', related_name='channels', on_delete=models.CASCADE)

    def __str__(self):
        return "{0} ({1})".format(self.title, self.username)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        token = self.bot.token
        bot = telegram.Bot(token=token)

        channel = bot.get_chat(self.username)

        self.channel_id = channel['id']
        self.type = channel['type']
        self.title = channel['title']

        super().save(force_insert, force_update, using, update_fields)


class Message(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    text = models.CharField(max_length=4096, null=True, blank=True)
    image = models.ImageField(upload_to=settings.MEDIA_ROOT, null=True, blank=True)
    send_time = models.DateTimeField()
    task_id = models.CharField(max_length=50, unique=True, null=True, default=None)
    owner = models.ForeignKey('auth.User', related_name='messages', on_delete=models.CASCADE)

    def __str__(self):
        return self.text or 'None'

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="/static/img/{0}" width="100" />'.format(self.image))

    image_tag.short_description = "Image preview"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        task = tasks.send_messages.apply_async(args=[self.channel.bot.token, self.channel.id, self.text or None,
                                                     None if not self.image else self.image.path],
                                               eta=self.send_time)
        if self.task_id:
            old_task = AsyncResult(self.task_id)
            old_task.revoke()

            self.task_id = task.id

        super().save(force_insert, force_update, using, update_fields)


# noinspection PyUnusedLocal
@receiver(models.signals.post_delete, sender=Message)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


# noinspection PyUnusedLocal
@receiver(models.signals.pre_save, sender=Message)
def auto_delete_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_image = Message.objects.get(pk=instance.pk).image
    except Message.DoesNotExist:
        return False

    new_image = instance.image
    if old_image and not old_image == new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)
