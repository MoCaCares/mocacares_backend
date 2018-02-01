import os
import shutil

from django.dispatch import receiver
from django.db import models
from .models_user import User


class UploadedImage(models.Model):
    image = models.ImageField()
    image_url = models.TextField()

    def save(self, *args, **kwargs):
        super(UploadedImage, self).save(*args, **kwargs) # Call the "real" save() method.
        self.image_url = self.image.url
        super(UploadedImage, self).save(*args, **kwargs) # Call the "real" save() method.


@receiver(models.signals.pre_delete, sender=UploadedImage)
def delete_local_file(sender, instance, **kwargs):
    """
    delete the corresponding image file
    """
    instance.image.delete(save=False)


class EventType(models.Model):
    name = models.TextField()


class Event(models.Model):
    title = models.CharField(max_length=1028)
    description = models.TextField()
    address = models.TextField()
    img = models.OneToOneField(UploadedImage, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='participated_event_set', blank=True)
    followers = models.ManyToManyField(User, related_name='bookmarked_event_set', blank=True)

    def __unicode__(self):
        return str(self.pk) + ". " + str(self.title) + ": " + self.description
    
    def delete(self, *args, **kwargs):
        self.img.delete()
        super(Event, self).delete(*args, **kwargs)


class Feedback(models.Model):
    content = models.TextField()


class Comment(models.Model):
    content = models.TextField()
    target_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)  # many Documents to one User
    post_time = models.DateTimeField(auto_now=False, auto_now_add=True)


class TokenVerificationPair(models.Model):
    token = models.CharField(max_length=32)
    verification_code = models.CharField(max_length=5)


