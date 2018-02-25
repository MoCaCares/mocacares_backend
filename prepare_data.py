import os, sys
import django

sys.path.append('./mocacares_backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mocacares_backend.settings')
django.setup()

from event_platform.models import *


for event in Event.objects.all():
    event.delete()

EventType(
    name='elderly cares',
).save()

EventType(
    name='five loaves',
).save()

EventType(
    name='paid jobs',
).save()

EventType(
    name='tuition aid',
).save()



for i in range(1,11):
    config = SystemConfig()
    config.save()
    org_user = User(
        username='org'+str(i),
        email_address=str(i)+'@org.com',
        user_type=2,
        system_config=config,
    )
    org_user.set_password('a123456')
    org_user.save()

    config = SystemConfig()
    config.save()
    vol_user = User(
        username='vol'+str(i),
        email_address=str(i)+'@vol.com',
        user_type=1,
        system_config=config,
    )
    vol_user.set_password('a123456')
    vol_user.save()


print(list(User.objects.all()))
print(list(EventType.objects.all()))
