from django.urls import path
from .views import *

urlpatterns = [
    path('register', RegisterApiView.as_view()),
    path('login', LoginView.as_view()),
    path('project', projectDetails.as_view()),
    path('project/<int:pk>', projectDetails.as_view()),
    path('task', TaskView.as_view()),
    path('task/<int:pk>', TaskView.as_view()),
    path('permission',PermissionsView.as_view()),
    path('permission/<int:pk>',PermissionsView.as_view()),
]