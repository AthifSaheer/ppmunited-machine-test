from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.hashers import make_password, check_password
from .serializers import UserCreateSerializer, UserLoginSerializer
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from .models import *

User = get_user_model()

@api_view(['GET'])
def api_over_view(request):
    if not request.user.is_authenticated:
        data = {
            "Create account API" : 'create/account/',
            "Login API" : '/login/',
        }
    else:
        data = {
            "Logout API" : '/logout/',
        }
    return Response(data, status=status.HTTP_200_OK) 

@api_view(['POST'])
def create_account(request):
    """
        {
            "username" : 'username',
            "role" : 'admin, staff, instructor, parent, student',
            "email" : 'email',
            "password" : 'password',
        }
    """
    if request.method == 'POST':
        try:
            role = request.data['role']
        except KeyError:
            return Response({"error": "role('admin, staff, instructor, parent, student') is required field!"}, status=status.HTTP_200_OK)

        del request.data['role']
        serializer = UserCreateSerializer(data=request.data)

        if serializer.is_valid():
            password = make_password(request.data['password'])
            serializer.save(password=password)
            user = User.objects.get(username=request.data['username'])
            if role == 'admin':
                user.is_admin = True
            if role == 'staff':
                user.is_staff = True
            if role == 'instructor':
                user.is_instructor = True
                instructor = Instructor()
                instructor.username = user.username
                instructor.email = user.email
                instructor.save()
            if role == 'parent':
                user.is_parent = True
            if role == 'student':
                user.is_student = True
                student = Student()
                student.username = user.username
                student.email = user.email
                student.save()
            user.save()

            user_ = authenticate(request, username=request.data['username'], password=request.data['password'])
            auth_login(request, user_)
            return Response({'Token': 'token-access'}, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_201_CREATED)
    
    return Response({"error": 'something went wrong'} ,status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
    """
        {
            "username" : "username,
            "password" : "password
        }
    """
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.data.get('username'))
            if user.check_password(request.data.get('password')):
                user_ = authenticate(request, username=request.data['username'], password=request.data['password'])
                auth_login(request, user_)
                return Response({'Token': 'token-access'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'invalid password'}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': 'invalid username'}, status=status.HTTP_201_CREATED)
    
    return Response({"error": 'something went wrong'} ,status=status.HTTP_200_OK)

@api_view(['GET'])
def logout(request):
    auth_logout(request)
    return Response({'Success': 'Logged-out successfully'}, status=status.HTTP_201_CREATED)
    