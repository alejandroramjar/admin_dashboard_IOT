# Generated by Django 4.2.15 on 2024-09-08 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='variable',
            name='limite_inferior',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='variable',
            name='limite_superior',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
