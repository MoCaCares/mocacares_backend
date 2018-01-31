from .models_user import *
from .models import *
from .models_chat import *


class TokenVerificationPair(models.Model):
    token = models.CharField(max_length=32)
    verification_code = models.CharField(max_length=5)
