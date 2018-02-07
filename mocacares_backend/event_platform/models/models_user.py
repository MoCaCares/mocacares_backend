import os
import shutil

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .models_common import UploadedImage


class SystemConfig(models.Model):
    recommend = models.IntegerField(default=1) # 1, 2, 3, 4
    notify = models.IntegerField(default=1) # 1, 2
    receive = models.IntegerField(default=1) # 1
    is_show_email = models.BooleanField(default=True)
    is_show_events = models.BooleanField(default=False)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email_address, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email_address = self.normalize_email(email_address)
        user = self.model(username=username, email_address=email_address, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email_address=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email_address, password, **extra_fields)

    def create_superuser(self, username, email_address, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 2)
        config = SystemConfig()
        config.save()
        extra_fields.setdefault('system_config', config)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email_address, password, **extra_fields)


def upload_to(instance, filename):
    name_without_extension, extension = filename.split(".")
    # if a user with sign-in email = user@email.com uploads file name.png
    # the file will be store at media/portrait/user@email.com/portrait.png
    return '{0}/{1}/{2}.{3}'.format("portrait", instance.email_address, "portrait", extension)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=254, unique=True)

    email_address = models.EmailField(max_length=254, unique=True)

    # field "password" inherited from AbstractBaseUser

    following_users = models.ManyToManyField("User", related_name="follower_set", blank=True, symmetrical=False)

    level = models.IntegerField(default=0)

    portrait = models.OneToOneField(UploadedImage, on_delete=models.CASCADE, null=True, blank=True)

    user_type = models.IntegerField()  # 1: volunteer; 2: organization

    system_config = models.OneToOneField(SystemConfig, on_delete=models.CASCADE)

    statement = models.TextField(default='')

    occupation = models.TextField(default='')
    
    age = models.IntegerField(default=0)

    gender = models.IntegerField(default=1)

    @property
    def portrait_url(self):
        if self.portrait and hasattr(self.portrait, 'url'):
            return self.portrait.url
        else:
            return "/media/portrait/default_portrait.png"

    USERNAME_FIELD = "email_address"

    REQUIRED_FIELDS = ["username"]

    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    def get_full_name(self):
        return self.username + "<" + self.email_address + ">" + "level:" + str(self.level) + " superuser:" + str(self.is_superuser) + " staff:" + str(self.is_staff)

    def get_short_name(self):
        return self.username

    def set_username(self, username):
        self.username = username

    def set_email_address(self, email_address):
        self.email_address = email_address

    # set_password method inherited from super class

    def __unicode__(self):
        return self.get_full_name()


@receiver(models.signals.pre_delete, sender=User)
# "sender" and "**kwargs" are required though they are of no use here, do not delete them
def delete_local_portrait(sender, instance, **kwargs):
    """
    delete the local image files for this user's portrait
    """
    if instance.portrait and hasattr(instance.portrait, 'url'):
        portrait = instance.portrait
        img_local_location = portrait.storage.path(portrait)
        img_local_dirname, file_name_and_extension = os.path.split(img_local_location)

        if os.path.isdir(img_local_dirname):
            shutil.rmtree(img_local_dirname)


# TODO:  if scale increase, use redis to store the verification code pair
class TokenVerificationPair(models.Model):
    token = models.CharField(max_length=32)
    verification_code = models.CharField(max_length=5)












