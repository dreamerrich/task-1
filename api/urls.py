from django.urls import path
from .views import *

urlpatterns = [
    path('register', RegisterApiView.as_view()),
    path('login', LoginView.as_view()),
    path('project', projectDetails.as_view()),
    path('details/<int:pk>', projectDetails.as_view()),
    path('task', TaskView.as_view()),
    path('task/<int:pk>', projectDetails.as_view()),
]