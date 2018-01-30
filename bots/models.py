from django.db import models


class Bot(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    username = models.CharField(max_length=32)
    token = models.CharField(max_length=45)
