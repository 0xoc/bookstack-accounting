from rest_framework import serializers

from accounting.models import *
from user_management.models import UserProfile
from django.contrib.auth.models import User, Group


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


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
        fields = [
            'user',
            'person_type',
            'national_id',
            'telephone',
            'address']

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
        fields = [
            'user',
            'person_type',
            'national_id',
            'telephone',
            'address',
        ]


class OrganizationCreateSerializer(serializers.ModelSerializer):
    shop_admin = UserProfileCreateSerializer()

    class Meta:
        model = Organization
        fields = [
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
        ]

    def create(self, validated_data):
        shop_admin_info = validated_data.pop('shop_admin')

        admin = UserProfileCreateSerializer(data=shop_admin_info)
        admin.is_valid()
        admin = admin.save()
        Group.objects.get(name="organization_admin").user_set.add(admin.user)

        organization = Organization(**validated_data)
        organization.save()
        organization.staff.add(admin)
        return organization


class OrganizationRetrieveSerializer(serializers.ModelSerializer):
    staff = UserProfileRetrieveSerializer(many=True)

    class Meta:
        model = Organization
        fields = [
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
        ]


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'organization',
            'name'
        ]


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


class TagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'code',
            'description'
        )

    def create(self, validated_data):
        tag = Tag(**validated_data)
        tag.save()
        return tag


class TagRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'code',
            'description'
        )


class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'account',
            'amount',
            'type',
        )

    def create(self, validated_data):
        transaction = Transaction(**validated_data)
        transaction.save()
        return transaction


class TransactionRetrieveSerializer(serializers.ModelSerializer):
    account = AccountRetrieveSerializer()

    class Meta:
        model = Transaction
        fields = (
            'account',
            'amount',
            'type',
        )


class AccountingDocumentCreateSerializer(serializers.ModelSerializer):
    transactions = TransactionCreateSerializer(many=True)

    class Meta:
        model = AccountingDocument
        fields = (
            'transactions',
            'number',
            'date_time',
            'tag',
        )

    def create(self, validated_data):
        transactions = validated_data.pop('transactions', None)
        accountDocument = AccountingDocument(**validated_data)
        org = self.context.get('organization')
        accountDocument.organization = org
        accountDocument.save()
        if transactions is not None:
            for transaction in transactions:
                transaction.account_document = accountDocument
        return accountDocument


class AccountingDocumentRetrieveSerializer(serializers.ModelSerializer):
    transactions = TransactionRetrieveSerializer(many=True)

    class Meta:
        model = AccountingDocument
        fields = (
            'transactions',
            'number',
            'date_time',
            'tag',
        )


class StaffCreateSerializer(serializers.Serializer):
    user_profile = UserProfileCreateSerializer()

    def create(self, validated_data):
        user_info = validated_data.pop('user_profile', None)

        staff = UserProfileCreateSerializer(data=user_info)
        staff.is_valid()
        staff = staff.save()
        Group.objects.get(name="organization_staff").user_set.add(staff.user)

        org = self.context.get('organization')
        org.staff.add(staff)

        return org
