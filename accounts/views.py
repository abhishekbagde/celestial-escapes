from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth.models import User
from .models import Profile
from .serializers import RegisterSerializer, UserSerializer, ProfileUpdateSerializer


class RegisterView(generics.CreateAPIView):
    """POST /api/v1/accounts/register/ — public"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {'message': f'Welcome, {user.username}! Your account has been created.'},
            status=status.HTTP_201_CREATED
        )


class MeView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/v1/accounts/me/ — current user info + update name/email"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ProfileUpdateView(APIView):
    """PATCH /api/v1/accounts/profile/ — update extended profile (avatar, bio, etc.)"""
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        profile = request.user.profile
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        profile = request.user.profile
        serializer = ProfileUpdateSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(request.user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
