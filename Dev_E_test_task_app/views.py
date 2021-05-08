from django.http import Http404
from django.contrib.auth.models import update_last_login

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import WriteOnlyUserSerializer, ReadOnlyUserSerializer, UserSerializer
from .models import MyUser


class TokenAuthenticationView(ObtainAuthToken):
    """Implementation of ObtainAuthToken with last_login update"""

    def post(self, request, *args, **kwargs):
        result = super(TokenAuthenticationView, self).post(request)
        try:
            token = Token.objects.get(key=result.data['token'])
            update_last_login(None, token.user)
        except Exception as exc:
            return None
        return result


class UsersRegistrationAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        users = MyUser.objects.all()
        serializer = ReadOnlyUserSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.data
        input_serializer = WriteOnlyUserSerializer(data=user)
        input_serializer.is_valid(raise_exception=True)
        input_serializer.save()
        db_query = MyUser.objects.get(username=user['username'])
        output_serializer = ReadOnlyUserSerializer(db_query)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ViewSet):

    def get_object(self, pk):
        try:
            return MyUser.objects.get(pk=pk)
        except MyUser.DoesNotExist:
            raise Http404

    def list(self, request):
        users = MyUser.objects.all()
        serializer = ReadOnlyUserSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        user = request.data
        input_serializer = WriteOnlyUserSerializer(data=user)
        input_serializer.is_valid(raise_exception=True)
        input_serializer.save()
        db_query = MyUser.objects.get(username=user['username'])
        output_serializer = ReadOnlyUserSerializer(db_query)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk):
        user_info = self.get_object(pk)
        serializer = ReadOnlyUserSerializer(user_info)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        user = self.get_object(pk)
        input_serializer = WriteOnlyUserSerializer(user, data=request.data)
        input_serializer.is_valid(raise_exception=True)
        input_serializer.save()

        db_query = self.get_object(pk)
        output_serializer = ReadOnlyUserSerializer(db_query)

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk):
        user = self.get_object(pk)
        input_serializer = WriteOnlyUserSerializer(user, data=request.data)
        input_serializer.is_valid(raise_exception=True)
        input_serializer.save()

        db_query = self.get_object(pk)
        output_serializer = ReadOnlyUserSerializer(db_query)

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        user = self.get_object(pk)
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
