# Generated by Django 4.2.6 on 2024-02-12 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_examform'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examform',
            name='display_countdown',
        ),
    ]
