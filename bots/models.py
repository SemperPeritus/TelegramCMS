from django.db import models


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
