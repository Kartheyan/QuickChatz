from __future__ import unicode_literals

from django.db import models

# Create your models here.


class ChatRoom(models.Model):
    room_id = models.CharField(max_length=8, blank=False, unique=True)
