from .models_user import *
from .models import *
from .models_chat import *
from django.db import models


class UploadedImage(models.Model):
    image = models.ImageField()

    @property
    def image_url(self):
        return self.image.url


@receiver(models.signals.pre_delete, sender=UploadedImage)
def delete_local_file(sender, instance, **kwargs):
    """
    delete the corresponding image file
    """
    instance.image.delete()
