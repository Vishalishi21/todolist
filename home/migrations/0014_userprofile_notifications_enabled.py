# Generated by Django 4.2.3 on 2023-12-29 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_rename_is_assigned_task_admin_assigned_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='notifications_enabled',
            field=models.BooleanField(default=True),
        ),
    ]
