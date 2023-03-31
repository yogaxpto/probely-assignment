from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField

from common.models import BaseModel


class User(AbstractUser, BaseModel):
    name = CharField(max_length=40)
