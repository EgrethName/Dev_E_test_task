from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)


class MyUserManager(BaseUserManager):

    def create_user(self, username, password=None, **kwargs):
        if username is None:
            raise TypeError('More then 1 symbol required in username')
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password):
        if password is None:
            raise TypeError('Password is required for superuser')
        user = self.create_user(username, password)
        user.is_superuser = True
        user.save()

        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=150, unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = MyUserManager()
