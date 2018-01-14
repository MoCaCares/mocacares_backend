import os
import shutil

from django.db import models
from .models_user import User



class Event(models.Model):
    title = models.CharField(max_length=1028)
    description = models.TextField()
    address = models.TextField()
    start_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return str(self.id) + ". " + str(self.title) + ": " + self.description


class Tag(models.Model):
    pass


class EventCategory(models.Model):
    pass


class Feedback(models.Model):
    content = models.TextField()


class Comment(models.Model):
    content = models.TextField()
    description = models.TextField()
    post_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    target_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)  # many Documents to one User


