# Generated by Django 5.0.4 on 2024-04-14 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0007_remove_planet_gltf_file_planet_object_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='planet',
            name='fare',
            field=models.FloatField(default=0.0),
        ),
    ]
