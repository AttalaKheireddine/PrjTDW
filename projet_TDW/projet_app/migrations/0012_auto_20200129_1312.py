# Generated by Django 2.1.1 on 2020-01-29 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projet_app', '0011_article'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='translationrequest',
            options={'verbose_name_plural': 'Devis de traduction'},
        ),
        migrations.AlterModelOptions(
            name='translationresponse',
            options={'verbose_name_plural': 'Traductions'},
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='translatorprofile',
            name='number_of_translations',
            field=models.IntegerField(default=0, verbose_name='Nombre de Traductions'),
        ),
    ]
