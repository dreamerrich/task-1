from rest_framework.response import Response
from  .serializers import *
from rest_framework.permissions import AllowAny
from .permissions import IsAdminOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
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
            if user is not None:
                payload = JWT_PAYLOAD_HANDLER(user)
                jwt_access_token_lifetime =  settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
                jwt_refresh_token_lifetime =  settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
                update_last_login(None, user)
                response = {
                            'access': str(token.access_token),
                            "access_token_life_time_in_seconds" : jwt_access_token_lifetime.total_seconds(),
                            'referesh_token':str(token),
                            "refresh_token_life_time_in_seconds" : jwt_refresh_token_lifetime.total_seconds(),
                        }
                status_code = status.HTTP_200_OK
                return Response(response, status=status_code)
            else:
                return Response({"error": 'Your password is not correct please try again or reset your password'}, status=401)

'''------------- CRUD operations ------------'''
class projectDetails(APIView):
    permission_classes = [IsAdminOrReadOnly, ]
        
    def get_object(self, pk):
        try:
            user = self.request.user
            return Project.objects.filter(created_by=user).get(pk=pk)
        except Project.DoesNotExist as e:
            raise Http404 from e

    def get(self, request, pk, format=None):
        project_data = self.get_object(pk)
        serializer = projectSerializer(project_data, context={'request':request})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = projectSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save(
                created_by = self.request.user 
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, pk, format=None):
        project_data = self.get_object(pk)
        serializer = projectSerializer(project_data, data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk, format=None):
        project_data = self.get_object(pk)
        serializer = projectSerializer(project_data, data=request.data, partial=True, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, format=None):
        project_data = self.get_object(pk)
        project_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_data(self, request):
        project_data = Project.objects.all()
        serializer = projectSerializer(project_data, many=True)
        return Response(serializer.data)
    
'''---------------task assigning---------------'''
class TaskView(APIView): 
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            user = self.request.user
            user_task = Task.objects.filter(assign_to=user).get(id=pk)
            return user_task
        except Task.DoesNotExist as e:
            raise Http404 from e

    def get(self, request, pk, format=None):
        task_data = self.get_object(pk)
        serializer = taskSerializer(task_data, context={'request':request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = taskSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save(
                assign_to = self.request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
    
    def patch(self, request, pk, format=None):
        task_data = self.get_object(pk)
        serializer = taskSerializer(task_data, data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk, format=None):
        task_data = self.get_object(pk)
        serializer = taskSerializer(task_data, data=request.data, partial=True, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, format=None):
        task_data = self.get_object(pk)
        task_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_data(self, request, format=None):
        task_data = Task.objects.all()
        serializer = taskSerializer(task_data, many=True)
        return Response(serializer.data)
    
'''---------------permission---------------'''
    
class PermissionsView(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self, request, format=None):
        serializer = permissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
    
    def get_data(self, request, format=None):
        user = self.request.user
        permission_data = Permission.objects.filter(name=user).all()
        serializer = permissionSerializer(permission_data, context={'request':request}, many=True)
        return Response(serializer.data)
    
    def get_object(self, pk):
        try:
            user = self.request.user
            user_role = Permission.objects.filter(name=user).get(project=pk)
            return user_role
        except Task.DoesNotExist as e:
            raise Http404 from e

    def get(self, request, pk, format=None):
        role_data = self.get_object(pk)
        serializer = permissionSerializer(role_data, context={'request':request})
        return Response(serializer.data)