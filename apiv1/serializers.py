from rest_framework import serializers

from accounting.models import *
from user_management.models import UserProfile
from django.contrib.auth.models import User


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('name',
                  'person_type',
                  'national_id',
                  'telephone',
                  'address',
                  'username',
                  'password')

    def validate_username(self, username):
        try:
            User.objects.get(username)
            raise serializers.ValidationError('username existed')
        except User.DoesNotExist:
            return username

    model = User
    fields = ('pk', 'username', 'first_name', 'last_name', 'email')


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')  # needs to be set by set_password

        user = User(**validated_data)
        user.set_password(password)
        user.is_staff = True  # so that user can log into django admin
        user.save()

        return user


class UserProfileCreateSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = UserProfile
        fields = (
            'user',
            'person_type',
            'national_id',
            'telephone',
            'address')

    def create(self, validated_data):
        user_info = validated_data.pop('user')  # pop user info from validated data
        user = UserCreateSerializer(data=user_info)  # create a new user with UserCreateSerializer

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
        fields = (
            'user',
            'person_type',
            'national_id',
            'telephone',
            'address',
        )


class OrganizationCreateSerializer(serializers.ModelSerializer):
    shop_admin = UserProfileCreateSerializer()

    class Meta:
        model = Organization
        fields = (
            'name',
            'alias_name',
            'national_id',
            'registration_id',
            'e_id',
            'description',
            'postal_address',
            'telephone',
            'fax',
            'email',
            'shop_admin',
        )

    def create(self, validated_data):
        shop_admin_info = validated_data.pop('shop_admin')

        admin = UserProfileCreateSerializer(data=shop_admin_info)
        admin.is_valid()
        admin = admin.save()

        organization = Organization(**validated_data)
        organization.save()
        organization.staff.add(admin)
        return organization


class OrganizationRetrieveSerializer(serializers.ModelSerializer):
    staff = UserProfileRetrieveSerializer(many=True)

    class Meta:
        model = Organization
        fields = (
            'name',
            'alias_name',
            'national_id',
            'registration_id',
            'e_id',
            'description',
            'postal_address',
            'telephone',
            'fax',
            'email',
            'staff',
        )


class ProductCreateSerializer(serializers.ModelSerializer):
    organization = OrganizationCreateSerializer()

    class Meta:
        model = Product
        fields = (
            'organization',
            'name'
        )

    def create(self, validated_data):
        organization_info = validated_data.pop('organization')
        organization = OrganizationCreateSerializer(data=organization_info)
        organization.is_valid()
        organization = organization.save()

        product = Product(**validated_data)
        product.save()
        product.organization = organization

        return product


class ProductRetrieveSerializer(serializers.ModelSerializer):
    organization = OrganizationRetrieveSerializer()

    class Meta:
        model = Product
        fields = (
            'organization',
            'name'
        )


class AccountCreateSerializer(serializers.ModelSerializer):
    # add accounts

    class Meta:
        model = Account
        fields = (
            'code',
            'title',
            'description',
            'type',
            'organization',
            'children'
        )

    def create(self, validated_data):
        # add children serializer

        account = Account(**validated_data)
        # add parent
        account.save()
        return account


## account retrieve serialzier

class AccountRetrieveSerializer(serializers.ModelSerializer):
    pass


class AccountingDocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountingDocument
        fields = (
            'number',
            'date_time',
            'description',
            'organization',
            'tag'
        )

    def create(self, validated_data):
        accounting_document = AccountingDocument(**validated_data)
        accounting_document.save()
        return accounting_document


class AccountingDocumentRetrieveSerializer(serializers.ModelSerializer):
    pass


class TransactionAccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'account',
            'amount',
            'type',
            'accounting_document',
        )

    def create(self, validated_data):
        transaction = Transaction(**validated_data)
        transaction.save()
        return transaction


class TransactionRetrieveSerializer(serializers.ModelSerializer):
    account = AccountRetrieveSerializer()
    accounting_document = AccountingDocumentRetrieveSerializer()

    class Meta:
        model = Transaction
        fields = (
            'account',
            'amount',
            'type',
            'accounting_document',
        )

#model manager
