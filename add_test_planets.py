#!/usr/bin/env python
"""
Script to add test planet data to the database
Run with: python manage.py shell < add_test_planets.py
Or: /Users/abhishekbagde/Documents/hack/celestial-escapes/.venv/bin/python add_test_planets.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spacetravel.settings')
django.setup()

from flight.models import Planet

# NASA GLTF 3D Models (stored locally)
planets_data = [
    {
        'name': 'Mars',
        'description': 'The Red Planet - Explore the vast canyons and ancient river valleys of Mars.',
        'object_url': '/media/models/mars.glb',
        'distance': 225.0,
        'fare': 50000.0,
        'emoji': '🔴'
    },
    {
        'name': 'Earth',
        'description': 'Our home planet - Experience the beauty of our world from space.',
        'object_url': '/media/models/earth.glb',
        'distance': 0.0,
        'fare': 25000.0,
        'emoji': '�'
    },
    {
        'name': 'Europa',
        'description': 'Jupiter\'s icy moon with a subsurface ocean - Explore potential for extraterrestrial life.',
        'object_url': '/media/models/europa.glb',
        'distance': 628.0,
        'fare': 75000.0,
        'emoji': '❄️'
    },
    {
        'name': 'Earth & Moon',
        'description': 'View the Earth-Moon system in stunning detail.',
        'object_url': '/media/models/earth_moon.glb',
        'distance': 0.384,
        'fare': 30000.0,
        'emoji': '🌙'
    },
]

# Clear existing planets
Planet.objects.all().delete()
print("✓ Cleared existing planets")

# Add new planets
for planet_info in planets_data:
    planet = Planet.objects.create(**planet_info)
    print(f"✓ Added planet: {planet.name} (${planet.fare})")

print(f"\n✅ Successfully added {len(planets_data)} test planets!")
print("\nNASA 3D Models loaded successfully!")
print("Models source: https://solarsystem.nasa.gov/resources/3d-models/")
