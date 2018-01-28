# Generated by Django 2.0.1 on 2018-01-28 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event_platform', '0013_auto_20180125_1711'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='systemconfig',
            name='target_user',
        ),
        migrations.AddField(
            model_name='systemconfig',
            name='id',
            field=models.AutoField(auto_created=True, default=2, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='system_config',
            field=models.OneToOneField(default=3, on_delete=django.db.models.deletion.CASCADE, to='event_platform.SystemConfig'),
            preserve_default=False,
        ),
    ]
