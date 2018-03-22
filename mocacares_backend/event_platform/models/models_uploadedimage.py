from django.db import models
from django.dispatch import receiver
from django.core.exceptions import ValidationError


def validate_file_size(f):
    limit = 5 * 1024 * 1024
    if f.size > limit:
        raise ValidationError('uploaded image size should be less than 5 mb.')

class UploadedImage(models.Model):
    image = models.ImageField()
    image_url = models.TextField(blank=True, default='')

    def save(self, *args, **kwargs):
        validate_file_size(self.image)
        super(UploadedImage, self).save(*args, **kwargs) # Call the "real" save() method.
        self.image_url = 'api/image/' + str(self.pk)
        super(UploadedImage, self).save(*args, **kwargs) # Call the "real" save() method.

@receiver(models.signals.pre_delete, sender=UploadedImage)
def delete_local_file(sender, instance, **kwargs):
    """
    delete the corresponding image file
    """
    instance.image.delete(save=False)





