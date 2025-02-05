import json

from django.shortcuts import get_list_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes


# Create your views here.

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def register_view(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email alrady exists'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    if len(password) < 6:
        return Response({'error': 'Password must be at least 6 characters long'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({'detail': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({'error': f'Issue registering the user: {str(e)}'}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and Password required'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    # Authenticate the user
    user = authenticate(username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def logout_view(request):
    # Get the token from the request
    token = request.auth

    # If the user is authenticated (token exists)
    if token:
        token.delete()  # Delete the token, logging the user out
        return Response({'detail': 'Successfully logged out'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'No active session found'}, status=status.HTTP_400_BAD_REQUEST)
    