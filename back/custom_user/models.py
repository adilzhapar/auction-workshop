from django.db import models
from django_use_email_as_username.models import BaseUser, BaseUserManager


class User(BaseUser):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth']
    objects = BaseUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
