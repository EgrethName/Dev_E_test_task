import re

from django.db.utils import IntegrityError
from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from .models import MyUser


class UserSerializer(serializers.ModelSerializer):
    is_superuser = serializers.BooleanField(default=False, read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)
    username = serializers.CharField(max_length=150, min_length=1, required=True)
    is_active = serializers.BooleanField(required=True)

    class Meta:
        model = MyUser
        fields = ['id', 'username', 'first_name', 'last_name', 'is_active', 'last_login', 'is_superuser', 'password']

    def create(self, validated_data):
        try:
            return MyUser.objects.create_user(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError('This username already exists')  # pylint: disable=raise-missing-from

    def update(self, instance, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().update(instance, validated_data)

    def validate_username(self, value):  # pylint: disable=no-self-use
        if re.match(r'^[\w.@+-]+$', value):
            return value

        raise serializers.ValidationError('Letters, digits and @/./+/-/_ only.')

    def validate_password(self, value):  # pylint: disable=no-self-use
        if re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', value):
            return value

        raise serializers.ValidationError('Incorrect password. Password should contain at least upper case letter, '
                                          'digit, and be longer than 8 characters')
