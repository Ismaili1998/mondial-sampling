from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=80, null=True)
    last_name = models.CharField(max_length=80, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    fax = models.CharField(max_length=50, blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
