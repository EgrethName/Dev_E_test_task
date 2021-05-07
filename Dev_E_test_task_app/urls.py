from django.contrib import admin
from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('api-token-auth', views.api_token_auth_create, name='api-token-auth'),
    path('api/v1/users', views.all_users_handler, name='all_users_handler'),
    re_path(r'api/v1/users/(?P<id>\d+)', views.user_handler, name='user_handler'),
]
