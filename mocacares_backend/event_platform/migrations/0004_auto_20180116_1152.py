# Generated by Django 2.0.1 on 2018-01-16 03:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_platform', '0003_remove_comment_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='followers',
            field=models.ManyToManyField(related_name='bookmarked_event_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(related_name='participated_event_set', to=settings.AUTH_USER_MODEL),
        ),
    ]