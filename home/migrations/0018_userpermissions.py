# Generated by Django 4.2.3 on 2024-01-03 10:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0017_remove_task_submitted_to_admin_task_submission'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPermissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can_add_task', models.BooleanField(default=False)),
                ('can_edit_task', models.BooleanField(default=False)),
                ('can_delete_task', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]