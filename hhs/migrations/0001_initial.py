# Generated by Django 3.2.9 on 2021-11-16 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HHSEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='date played')),
                ('where', models.CharField(max_length=10)),
                ('score', models.IntegerField(default=72)),
                ('cr', models.DecimalField(decimal_places=1, default=72.0, max_digits=3)),
                ('slope', models.IntegerField(default=135)),
            ],
        ),
    ]
