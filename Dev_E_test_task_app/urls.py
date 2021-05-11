from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import UserListCreateViewSet, UserModelViewSet, TokenAuthenticationView


app_name = 'Dev_E_test_task_app'


user_list = UserListCreateViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
user_detail = UserModelViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns([
    path('api-token-auth/', TokenAuthenticationView.as_view(), name='api-token-auth'),
    path('api/v1/users/', user_list, name='user-list'),
    path('api/v1/users/<int:pk>/', user_detail, name='user-detail'),
])
