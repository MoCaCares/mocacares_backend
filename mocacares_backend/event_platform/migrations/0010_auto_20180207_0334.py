# Generated by Django 2.0.1 on 2018-02-06 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_platform', '0009_auto_20180204_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='user',
            name='occupation',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='user',
            name='statement',
            field=models.TextField(default=''),
        ),
    ]