# Generated by Django 2.0.1 on 2018-01-16 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_platform', '0004_auto_20180116_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.DateTimeField(),
        ),
    ]
