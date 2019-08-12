from django.core.exceptions import ValidationError
from rest_framework import serializers
from user_management.models import UserProfile
from django.contrib.auth.models import User


class UserRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['pk', 'username', 'first_name', 'last_name', 'email']


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')  # needs to be set by set_password

        user = User(**validated_data)
        user.set_password(password)
        user.is_staff = True                       # so that user can log into django admin
        user.save()

        return user


class UserProfileCreateSerializer(serializers.ModelSerializer):

    user = UserCreateSerializer()

    class Meta:
        model = UserProfile
        fields = [
            'user',
            'person_type',
            'national_id',
            'telephone',
            'address']

    def create(self, validated_data):
        user_info = validated_data.pop('user')          # pop user info from validated data
        user = UserCreateSerializer(data=user_info)     # create a new user with UserCreateSerializer

        # must be called. don't need to check the result, data is coming from validated data, so it's valid
        user.is_valid()

        # get the new user instance
        user = user.save()

        user_profile = UserProfile(**validated_data)
        user_profile.user = user

        user_profile.save()
        return user_profile


class UserProfileRetrieveSerializer(serializers.ModelSerializer):

    user = UserRetrieveSerializer()

    class Meta:
        model = UserProfile
        fields = [
            'user',
            'person_type',
            'national_id',
            'telephone',
            'address',
        ]
