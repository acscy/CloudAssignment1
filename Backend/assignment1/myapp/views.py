from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer
from django.contrib.auth import authenticate, login, logout


@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        login(request, user)  # Log the user in
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']  # Access the user object from validated_data
        login(request, user)
        user_data = UserSerializer(user).data  # Serialize user instance
        return Response({"message": "User Logged In Successfully", "user": user_data}, status=status.HTTP_200_OK)
    else:
            return Response({"message": "Invalid username/password."}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_user(request):
    # Django's logout function removes the user from the session
    logout(request)
    return Response({"message": "User logged out successfully"}, status=status.HTTP_200_OK)