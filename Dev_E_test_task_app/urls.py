from django.urls import path, re_path
from rest_framework.authtoken import views
from rest_framework.urlpatterns import format_suffix_patterns

from .views import UsersRegistrationAPIView, UserViewSet, UserModelViewSet, TokenAuthenticationView


app_name = 'Dev_E_test_task_app'

user_list = UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

user_list1 = UserModelViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
user_detail1 = UserModelViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns([
    # path('api/v1/users/', UsersRegistrationAPIView.as_view()),
    path('api-token-auth/', TokenAuthenticationView.as_view()),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail'),
    path('users1/', user_list1, name='user-list'),
    path('users1/<int:pk>/', user_detail1, name='user-detail'),
])
