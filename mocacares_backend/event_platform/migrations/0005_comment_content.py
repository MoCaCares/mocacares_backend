# Generated by Django 2.0.1 on 2018-01-28 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_platform', '0004_remove_comment_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='content',
            field=models.TextField(default='wowwow'),
            preserve_default=False,
        ),
    ]
