from rest_framework import serializers
from user_management.models import UserProfile
from django.db import models
from django.contrib.auth.models import User


class UserProfileCreateSerializer(serializers.ModelSerializer):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    class Meta:
        model = UserProfile
        fields = ['name',
                  'person_type',
                  'national_id',
                  'telephone',
                  'address',
                  'username',
                  'password']

    def validate_username(self, username):
        try:
            User.objects.get(username)
            raise serializers.ValidationError('username existed')
        except User.DoesNotExist:
            return username

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')

        user = User(username=username)
        user.set_password(password)
        user.save()

        userProfile = UserProfile(**validated_data)
        userProfile.user = user

        userProfile.save()
        return userProfile
