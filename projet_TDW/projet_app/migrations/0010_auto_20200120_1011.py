# Generated by Django 2.1.1 on 2020-01-20 09:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projet_app', '0009_auto_20200120_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='warn',
            name='treated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='warn',
            name='warn_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
