from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import Profile
from .models import Planet, Flight, Pod, Booking


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'avatar', 'bio', 'passport_id', 'preferred_pod_type', 'credits_balance', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PlanetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planet
        fields = ['id', 'name', 'slug', 'description', 'gltf_model_url', 'distance_from_earth_km', 
                  'travel_time_days', 'emoji', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


class PodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pod
        fields = ['id', 'flight', 'pod_number', 'pod_type', 'price_credits', 'is_available', 'created_at']
        read_only_fields = ['id', 'created_at']


class FlightSerializer(serializers.ModelSerializer):
    origin_planet = PlanetSerializer(read_only=True)
    destination_planet = PlanetSerializer(read_only=True)
    pods = PodSerializer(many=True, read_only=True)
    origin_planet_id = serializers.IntegerField(write_only=True)
    destination_planet_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Flight
        fields = ['id', 'flight_number', 'origin_planet', 'destination_planet', 'origin_planet_id', 
                  'destination_planet_id', 'departure_datetime', 'arrival_datetime', 'seats_total', 
                  'seats_available', 'price_credits', 'status', 'pods', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        origin_id = validated_data.pop('origin_planet_id')
        destination_id = validated_data.pop('destination_planet_id')
        validated_data['origin_planet_id'] = origin_id
        validated_data['destination_planet_id'] = destination_id
        return super().create(validated_data)


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    flight = FlightSerializer(read_only=True)
    pod = PodSerializer(read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'user', 'flight', 'pod', 'status', 'total_price', 'booked_at', 'updated_at']
        read_only_fields = ['id', 'user', 'booked_at', 'updated_at']
