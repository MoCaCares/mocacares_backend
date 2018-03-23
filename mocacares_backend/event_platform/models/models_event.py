import os
import shutil

from django.dispatch import receiver
from django.db import models
from .models_uploadedimage import UploadedImage
from .models_user import User


class EventType(models.Model):
    name = models.TextField(null=True, blank=True)
    img = models.OneToOneField(UploadedImage, on_delete=models.SET_NULL, null=True, blank=True)

    def __unicode__(self):
        return str(self)

    def __str__(self):
        return str(self.pk) + ". " + str(self.name)


class Event(models.Model):
    title = models.CharField(max_length=1028)
    description = models.TextField()
    address = models.TextField(null=True, blank=True)
    img = models.OneToOneField(UploadedImage, on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='participated_event_set', blank=True)
    followers = models.ManyToManyField(User, related_name='bookmarked_event_set', blank=True)

    def __unicode__(self):
        return str(self)
    
    def __str__(self):
        return str(self.pk) + ". " + str(self.title) + ": " + self.description


@receiver(models.signals.pre_delete, sender=Event)
def delete_attaching_image(sender, instance, **kwargs):
    if instance.img is not None:
        instance.img.delete()


class Feedback(models.Model):
    content = models.TextField()


class Comment(models.Model):
    content = models.TextField()
    target_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)  # many Documents to one User
    post_time = models.DateTimeField(auto_now=False, auto_now_add=True)


