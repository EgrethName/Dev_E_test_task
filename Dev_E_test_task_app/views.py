from django.contrib.auth.models import update_last_login

from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import UserSerializer
from .models import MyUser
from .permissions import IsOwnerOrReadOnly


class TokenAuthenticationView(ObtainAuthToken):
    """
    ObtainAuthToken-based class with updating last_login
    """

    def post(self, request, *args, **kwargs):
        result = super().post(request)
        token = Token.objects.get(key=result.data['token'])
        update_last_login(None, token.user)
        return result


class UserListCreateViewSet(viewsets.GenericViewSet,  # pylint: disable=too-many-ancestors
                            viewsets.mixins.CreateModelMixin,
                            viewsets.mixins.ListModelMixin):
    """
    Allow creating a new user without authentication
    """
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer


class UserModelViewSet(viewsets.GenericViewSet,  # pylint: disable=too-many-ancestors
                       viewsets.mixins.RetrieveModelMixin,
                       viewsets.mixins.UpdateModelMixin,
                       viewsets.mixins.DestroyModelMixin):
    """
    Only authenticated users can perform write operations with user
    """
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_destroy(self, instance):
        # we shouldn't delete the instance from DB on delete. Mark the `is_active` field as False instead
        instance.is_active = False
        instance.save()
        try:
            # remove a token for an 'deleted' user
            token = Token.objects.get(user=instance)
            token.delete()
        except Token.DoesNotExist:
            pass
