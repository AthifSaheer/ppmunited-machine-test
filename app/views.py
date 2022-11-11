from django.shortcuts import render
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from .serializers import UserCreateSerializer, UserLoginSerializer

User = get_user_model()

@api_view(['GET'])
def api_over_view(request):
    data = {
        "Create account API" : 'create/account/',
        "Login API" : '/login/',
        "User details API" : '/user/details/<token>/',
    }
    return Response(data, status=status.HTTP_200_OK) 

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

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

            return Response({'Token': 'new token'}, status=status.HTTP_201_CREATED)
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
                return Response({'Token': 'new token'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'invalid password'}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': 'invalid username'}, status=status.HTTP_201_CREATED)
    
    return Response({"error": 'something went wrong'} ,status=status.HTTP_200_OK)
