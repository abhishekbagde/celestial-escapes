# Generated by Django 5.0.4 on 2024-04-13 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='planet',
            name='distance',
            field=models.IntegerField(default=0),
        ),
    ]
