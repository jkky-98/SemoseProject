# Generated by Django 4.2.7 on 2023-11-06 05:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_logentry_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='logentry',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
