import os, sys
import django

sys.path.append('./mocacares_backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mocacares_backend.settings')
django.setup()

from event_platform.models import *



for i in range(1,11):
    org_user = User(
        username='org'+str(i),
        email_address=str(i)+'@org.com',
        user_type=2,
    )
    org_user.set_password('a123456')
    org_user.save()
    vol_user = User(
        username='vol'+str(i),
        email_address=str(i)+'@vol.com',
        user_type=1,
    )
    vol_user.set_password('a123456')
    vol_user.save()

for i in range(1,11):
    event_type = EventType(
        name='type'+str(i),
    )
    event_type.save()



print(list(User.objects.all()))
print(list(EventType.objects.all()))