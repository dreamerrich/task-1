from rest_framework.response import Response
from  .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework import generics
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser,Project
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import filters
from django.http import Http404

# Create your views here.

'''--------------- Class based view to register user -----------------'''
class RegisterApiView(APIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def get(self, request):
        queryset = User.objects.all()
        serializer_class = RegisterSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def post(self, request):
        serializer_class = RegisterSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


''' ------------- login view -----------------'''
class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def get(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            username = request.data.get("username", None)
            password = request.data.get("password")
            
            try:
                user = User.objects.get(username=username)
            except:
                user = None
                return Response({"error": "Your username is not correct. Please try again or register your details"})
            token = RefreshToken.for_user(user)

            user = authenticate(username=username, password=password)
            print("🚀 ~ file: views.py ~ line 42 ~ user", user)
            if user is not None:
                payload = JWT_PAYLOAD_HANDLER(user)
                jwt_access_token_lifetime =  settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
                jwt_refresh_token_lifetime =  settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
                update_last_login(None, user)
                response = {
                            'access': str(token.access_token),
                            'referesh_token':str(token),
                            "access_token_life_time_in_seconds" : jwt_access_token_lifetime.total_seconds(),
                            "refresh_token_life_time_in_seconds" : jwt_refresh_token_lifetime.total_seconds(),
                        }
                status_code = status.HTTP_200_OK
                return Response(response, status=status_code)
            else:
                return Response({"error": 'Your password is not correct please try again or reset your password'}, status=401)

'''------------- CRUD operations ------------'''
class projectDetails(APIView):
    permission_classes = (IsAuthenticated, )
    def get_object(self, pk):
        print("🚀 ~ file: views.py ~ line 44 ~ id", pk)
        try:
            user = self.request.user
            return Project.objects.filter(created_by=user).get(pk=pk)
        except Project.DoesNotExist as e:
            raise Http404 from e

    def get(self, request, pk, format=None):
        project_data = self.get_object(pk)
        print("🚀 ~ file: views.py ~ line 55 ~ project_data", project_data)
        serializer = projectSerializer(project_data, context={'request':request})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = projectSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save(
                created_by = self.request.user 
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        project_data = self.get_object(pk)
        serializer = projectSerializer(project_data, data=request.data)
        print("🚀 ~ file: views.py ~ line 63 ~ serializer", serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        project_data = self.get_object(pk)
        serializer = projectSerializer(project_data, data=request.data, partial=True)
        print("🚀 ~ file: views.py ~ line 62 ~ serializer", serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project_data = self.get_object(pk)
        project_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
'''---------------task assigning---------------'''
class TaskView(APIView): 
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, format=None):
        project_data = Task.objects.all()
        print("🚀 ~ file: views.py ~ line 55 ~ project_data", project_data)
        serializer = taskSerializer(project_data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        project = Project.objects.get()
        serializer = taskSerializer(data=request.data, context={'request':request})
        if project.created_by != self.request.user:
           return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        print("🚀 ~ file: views.py ~ line 44 ~ id", pk)
        try:
            user = self.request.user
            return Task.objects.filter(project=user).get(pk=pk)
        except Project.DoesNotExist as e:
            raise Http404 from e

    def get(self, request, pk, format=None):
        project_data = self.get_object(pk)
        print("🚀 ~ file: views.py ~ line 55 ~ project_data", project_data)
        serializer = projectSerializer(project_data, context={'request':request})
        return Response(serializer.data)
    
    def patch(self, request, pk, format=None):
        project_data = self.get_object(pk)
        serializer = taskSerializer(project_data, data=request.data)
        print("🚀 ~ file: views.py ~ line 63 ~ serializer", serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        project_data = self.get_object(pk)
        serializer = taskSerializer(project_data, data=request.data, partial=True)
        print("🚀 ~ file: views.py ~ line 62 ~ serializer", serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project_data = self.get_object(pk)
        project_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)