# Generated by Django 2.0.1 on 2018-02-03 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_platform', '0003_uploadedimage_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='read',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
