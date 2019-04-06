from django.db import models
from  django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User

class UserProfile(AbstractBaseUser):
    user = models.OneToOneField(User,  on_delete = models.CASCADE)
    accountType = models.CharField(max_length=20)