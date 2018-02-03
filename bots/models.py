import os
from django.db import models
from django.dispatch import receiver
from django.utils.safestring import mark_safe

from TelegramCMS import settings


class Bot(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    username = models.CharField(max_length=32)
    token = models.CharField(max_length=45)

    def __str__(self):
        return "{0} (@{1})".format(self.name, self.username)


class Channel(models.Model):
    id = models.BigIntegerField(primary_key=True)
    type = models.CharField(max_length=32)
    title = models.CharField(max_length=128)
    username = models.CharField(max_length=32)
    bot = models.ForeignKey(Bot, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "{0} ({1})".format(self.title, self.username)


class Message(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    text = models.CharField(max_length=4096, null=True, blank=True)
    image = models.ImageField(settings.MEDIA_ROOT, null=True, blank=True)
    send_time = models.DateTimeField()

    def __str__(self):
        return self.text

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="/static/img/{0}" width="100" />'.format(self.image))

    image_tag.short_description = "Image preview"


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
    if not old_image == new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)
