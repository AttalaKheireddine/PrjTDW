# Generated by Django 2.1.1 on 2020-01-13 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projet_app', '0002_auto_20200112_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='commune',
            field=models.CharField(default='Bouguirat', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='wilaya',
            field=models.CharField(default='Mostaganem', max_length=30),
            preserve_default=False,
        ),
    ]