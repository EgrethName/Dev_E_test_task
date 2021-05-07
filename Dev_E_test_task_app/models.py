from django.db import models


class AuthToken(models.Model):
    username = None
    password = None


class ReadOnlyUserSerializer(models.Model):
    id = None
    username = None
    first_name = None
    last_name = None
    is_active = None
    last_login = None
    is_superuser = None


class WriteOnlyUserSerializer(models.Model):
    username = None
    first_name = None
    last_name = None
    password = None
    is_active = None
