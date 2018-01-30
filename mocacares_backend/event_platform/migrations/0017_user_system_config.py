# Generated by Django 2.0.1 on 2018-01-29 07:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event_platform', '0016_remove_user_system_config'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='system_config',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='event_platform.SystemConfig'),
            preserve_default=False,
        ),
    ]