# Generated by Django 4.2.3 on 2023-12-05 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_status_alter_task_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='task',
            name='Status',
            field=models.CharField(max_length=50),
        ),
    ]
