# Generated by Django 4.2.3 on 2023-12-04 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='status',
            new_name='Status',
        ),
    ]