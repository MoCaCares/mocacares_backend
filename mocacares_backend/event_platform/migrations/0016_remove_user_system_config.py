# Generated by Django 2.0.1 on 2018-01-29 07:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event_platform', '0015_merge_20180129_1505'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='system_config',
        ),
    ]