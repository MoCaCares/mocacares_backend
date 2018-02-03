from django.db import models
from .models_user import User


class Message(models.Model):
    content = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sended_msg_set')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_msg_set')
    post_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    read = models.BooleanField()

    def __unicode__(self):
        return str(self.pk) + ". " + self.content


