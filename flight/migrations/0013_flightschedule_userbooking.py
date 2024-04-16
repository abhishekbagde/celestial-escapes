# Generated by Django 5.0.4 on 2024-04-14 07:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0012_remove_baseimage_base_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlightSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_number', models.CharField(max_length=20)),
                ('departure_date', models.DateField()),
                ('departure_time', models.TimeField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('arrival_date', models.DateField()),
                ('arrival_time', models.TimeField()),
                ('destination_base', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_flights', to='flight.planetbase')),
            ],
        ),
        migrations.CreateModel(
            name='UserBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=20)),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('ticket_type', models.CharField(max_length=20)),
                ('departure_date', models.DateField()),
                ('departure_time', models.TimeField()),
                ('return_date', models.DateField(blank=True, null=True)),
                ('return_time', models.TimeField(blank=True, null=True)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('arrival_base', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='UserBookingsArrival', to='flight.planetbase')),
                ('destination_base', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='UserBookingsDestination', to='flight.planetbase')),
                ('flight_schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.flightschedule')),
            ],
        ),
    ]