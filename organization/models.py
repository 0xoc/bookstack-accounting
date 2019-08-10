from django.db import models
from user_management.models import UserProfile
# Create your models here.


class Organization(models.Model):
    admin = 
    name = models.CharField(max_length=255)
    alias_name = models.CharField(max_length=255, blank=True, null=True)
    