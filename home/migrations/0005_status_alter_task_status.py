# Generated by Django 4.2.3 on 2023-12-05 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_task_status_delete_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='task',
            name='Status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.status'),
        ),
    ]
