from django.db import models
from django.dispatch import receiver


class UploadedImage(models.Model):
    image = models.ImageField()
    image_url = models.TextField(blank=True, default='')

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





