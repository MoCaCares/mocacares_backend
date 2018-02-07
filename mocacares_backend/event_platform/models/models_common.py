from django.db import models


class UploadedImage(models.Model):
    image = models.ImageField(null=True, blank=True)
    image_url = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super(UploadedImage, self).save(*args, **kwargs) # Call the "real" save() method.
        self.image_url = self.image.url
        super(UploadedImage, self).save(*args, **kwargs) # Call the "real" save() method.
