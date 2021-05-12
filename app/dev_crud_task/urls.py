from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from dev_crud_task_app.views import UserModelViewSet


router = DefaultRouter()
router.register('users', UserModelViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dev_crud_task_app.urls', namespace='dev_crud_task_app')),
]

urlpatterns += router.urls
