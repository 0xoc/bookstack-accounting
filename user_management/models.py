from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    person_type_choices = ((0, 'نامشخص'),
                           (1, 'حقیقی'),
                           (2, 'حقوقی'))

    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_profile")
    person_type = models.CharField(choices=person_type_choices, max_length=1)
    national_id = models.CharField(max_length=20, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
