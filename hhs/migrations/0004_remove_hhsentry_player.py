# Generated by Django 3.2.9 on 2021-11-26 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hhs', '0003_auto_20211126_1521'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hhsentry',
            name='player',
        ),
    ]
