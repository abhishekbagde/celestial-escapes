from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    avatar_url = serializers.ReadOnlyField()

    class Meta:
        model = Profile
        fields = [
            'id', 'bio', 'passport_id', 'phone', 'date_of_birth',
            'credits_balance', 'preferred_pod_type', 'avatar_url',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['credits_balance', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']
        read_only_fields = ['id']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Used for PATCH /api/v1/accounts/profile/"""
    class Meta:
        model = Profile
        fields = ['bio', 'passport_id', 'phone', 'date_of_birth', 'preferred_pod_type', 'avatar']
