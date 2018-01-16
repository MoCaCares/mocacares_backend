import os
import shutil

from django.db import models
from .models_user import User


class EventType(models.Model):
    name = models.TextField()


class Event(models.Model):
    title = models.CharField(max_length=1028)
    description = models.TextField()
    address = models.TextField()
    start_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)

    def __unicode__(self):
        return str(self.pk) + ". " + str(self.title) + ": " + self.description


class Feedback(models.Model):
    content = models.TextField()


class Comment(models.Model):
    content = models.TextField()
    target_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)  # many Documents to one User
    post_time = models.DateTimeField(auto_now=False, auto_now_add=True)


