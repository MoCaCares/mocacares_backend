# Generated by Django 2.0.1 on 2018-01-25 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_platform', '0012_event_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='img',
            field=models.CharField(max_length=256),
        ),
    ]