from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from flight.models import Planet, Flight, Pod, PlanetBase
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Seed the database with planets, flights, pods, and bases'

    def handle(self, *args, **options):
        self.stdout.write('Starting database seeding...')

        # Create demo user
        demo_user, created = User.objects.get_or_create(
            username='demo',
            defaults={
                'email': 'demo@example.com',
                'first_name': 'Demo',
                'last_name': 'User',
                'is_staff': False,
            }
        )
        if created:
            demo_user.set_password('demo123')
            demo_user.save()
            self.stdout.write(self.style.SUCCESS('✓ Created demo user'))
        else:
            self.stdout.write('✓ Demo user already exists')

        # Planet data with 30 planets from our solar system and beyond
        planets_data = [
            ('Earth', 'earth', 'Our home planet. Blue marble with diverse ecosystems.', 0, 0, '🌍', 100000),
            ('Mars', 'mars', 'The red planet. Known for its thin atmosphere and polar ice caps.', 225000000, 250, '🔴', 50000),
            ('Venus', 'venus', 'Hot and hostile planet with extreme atmospheric pressure.', 108000000, 150, '✨', 45000),
            ('Mercury', 'mercury', 'The smallest planet, closest to the sun.', 77000000, 120, '⚡', 40000),
            ('Jupiter', 'jupiter', 'Gas giant with the Great Red Spot. Largest planet in our system.', 550000000, 600, '🪐', 75000),
            ('Saturn', 'saturn', 'The ringed planet. Known for its spectacular ring system.', 1200000000, 800, '💫', 85000),
            ('Uranus', 'uranus', 'Ice giant with extreme winds and a tilted rotation axis.', 2600000000, 1200, '🌀', 95000),
            ('Neptune', 'neptune', 'Furthest ice giant with supersonic winds.', 4500000000, 1600, '🌊', 100000),
            ('Moon', 'moon', "Earth's natural satellite. Gateway to space.", 384400, 3, '🌙', 10000),
            ('Europa', 'europa', "Jupiter's icy moon with a hidden subsurface ocean.", 550000000, 620, '❄️', 80000),
            ('Titan', 'titan', "Saturn's largest moon with methane lakes.", 1200000000, 820, '🏜️', 90000),
            ('Proxima Centauri b', 'proxima-centauri-b', 'Exoplanet in the habitable zone of Proxima Centauri.', 40000000000000, 2000, '🌟', 500000),
            ('TRAPPIST-1e', 'trappist-1e', 'Earth-sized exoplanet in habitable zone.', 39000000000000, 1900, '🪐', 480000),
            ('Kepler-452b', 'kepler-452b', 'Earth cousin in the habitable zone of Kepler-452.', 1200000000000, 1800, '🌎', 450000),
            ('Enceladus', 'enceladus', "Saturn's icy moon with subsurface water.", 1200000000, 830, '🧊', 88000),
            ('Io', 'io', "Jupiter's most volcanically active moon.", 550000000, 610, '🌋', 78000),
            ('Ganymede', 'ganymede', "Jupiter's largest moon, larger than Mercury.", 550000000, 630, '🎯', 82000),
            ('Callisto', 'callisto', "Jupiter's heavily cratered moon.", 550000000, 640, '🎲', 81000),
            ('Mimas', 'mimas', "Saturn's moon famous for its giant impact crater.", 1200000000, 810, '⭕', 87000),
            ('Rhea', 'rhea', "Saturn's second-largest moon.", 1200000000, 815, '⚪', 88500),
            ('Iapetus', 'iapetus', "Saturn's moon with unusual two-tone coloring.", 1200000000, 825, '🍪', 89000),
            ('Triton', 'triton', "Neptune's largest moon with nitrogen geysers.", 4500000000, 1620, '❄️', 102000),
            ('Pluto', 'pluto', 'Dwarf planet with icy terrain and nitrogen plains.', 5900000000, 1800, '🧊', 110000),
            ('Ceres', 'ceres', 'Dwarf planet in the asteroid belt.', 414000000, 500, '🪨', 65000),
            ('Vesta', 'vesta', 'Large asteroid with diverse terrain.', 250000000, 300, '⛰️', 35000),
            ('Juno', 'juno', 'Bright asteroid in the asteroid belt.', 300000000, 350, '✨', 38000),
            ('Apophis', 'apophis', 'Near-Earth asteroid with unique characteristics.', 10000000, 45, '🌠', 25000),
            ('Phoebe', 'phoebe', "Saturn's irregular moon.", 1200000000, 850, '🪨', 90000),
            ('Miranda', 'miranda', "Uranus's moon with extreme terrain variations.", 2600000000, 1220, '🗻', 98000),
            ('Oberon', 'oberon', "Uranus's largest moon.", 2600000000, 1230, '👑', 99000),
        ]

        # Create planets
        planets = {}
        for name, slug, description, distance, travel_time, emoji, flight_price in planets_data:
            planet, created = Planet.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'description': description,
                    'distance_from_earth_km': distance,
                    'travel_time_days': travel_time,
                    'emoji': emoji,
                }
            )
            planets[slug] = (planet, flight_price)
            if created:
                self.stdout.write(f'✓ Created planet: {planet.name}')

        # Create bases on planets
        bases_data = [
            ('earth', 'Kennedy Space Center', 'Florida, USA'),
            ('earth', 'Baikonur Cosmodrome', 'Kazakhstan'),
            ('earth', 'Spaceport America', 'New Mexico, USA'),
            ('moon', 'Lunar Base One', 'South Pole'),
            ('moon', 'Mare Tranquillitatis', 'Apollo 11 Landing Site'),
            ('mars', 'Olympus Mons Station', 'Largest Volcano'),
            ('mars', 'Valles Marineris Base', 'Canyon System'),
            ('europa', 'Europa Station', 'Ice Surface'),
            ('titan', 'Titan Research Base', 'Methane Lakes'),
            ('saturn', 'Saturn Orbital Station', 'Upper Atmosphere'),
        ]

        for planet_slug, base_name, description in bases_data:
            if planet_slug in planets:
                planet, _ = planets[planet_slug]
                base, created = PlanetBase.objects.get_or_create(
                    planet=planet,
                    name=base_name,
                    defaults={
                        'description': description,
                    }
                )
                if created:
                    self.stdout.write(f'✓ Created base: {base.name}')

        # Pod types and data
        pod_types = [
            {'type': 'standard', 'price': 5000},
            {'type': 'luxury', 'price': 15000},
            {'type': 'cryo', 'price': 10000},
        ]

        # Create flights
        now = timezone.now()
        flight_count = 0
        planet_slugs = list(planets.keys())
        
        for i, source_slug in enumerate(planet_slugs[:5]):
            for dest_slug in planet_slugs[i+1:6]:
                source, _ = planets[source_slug]
                destination, base_fare = planets[dest_slug]
                
                # Create 2-3 flights per route
                for j in range(random.randint(2, 3)):
                    flight_time = now + timedelta(days=random.randint(5, 60))
                    
                    flight = Flight.objects.create(
                        flight_number=f'FL{source.name[:3].upper()}-{destination.name[:3].upper()}-{j+1}',
                        origin_planet=source,
                        destination_planet=destination,
                        departure_datetime=flight_time,
                        arrival_datetime=flight_time + timedelta(days=destination.travel_time_days),
                        seats_total=200,
                        seats_available=random.randint(10, 150),
                        price_credits=base_fare + random.randint(-5000, 10000),
                        status='scheduled',
                    )
                    
                    # Create pods for this flight - ensure unique pod numbers per flight
                    pod_counter = 1
                    for pod_type_info in pod_types:
                        for _ in range(random.randint(3, 6)):
                            Pod.objects.create(
                                flight=flight,
                                pod_number=str(pod_counter),
                                pod_type=pod_type_info['type'],
                                price_credits=pod_type_info['price'],
                                is_available=random.choice([True, True, False]),
                            )
                            pod_counter += 1
                    
                    flight_count += 1
                    self.stdout.write(f'✓ Created flight: {flight.flight_number}')

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Database seeding completed!\n'
                f'  - {len(planets)} planets created\n'
                f'  - {flight_count} flights created\n'
                f'  - Demo user: demo@example.com / demo123'
            )
        )
