from django.db import models
from django_jalali.db import models as jmodels
from user_management.models import UserProfile
from tag.models import Tag

# Create your models here.


account_types = ((0,'گروه اصلی'),
                 (1, 'حساب کل'),
                 (2, 'حساب معین'),
                 (3, 'تفصیلی'))


class Organization(models.Model):
    name = models.CharField(max_length=255)
    alias_name = models.CharField(max_length=255, blank=True, null=True)
    national_id = models.CharField(max_length=255, blank=True, null=True)
    registration_id = models.CharField(max_length=255, blank=True, null=True)
    e_id = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    postal_address = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    staff = models.ManyToManyField(UserProfile, related_name="organization")


class Product(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)


class Account(models.Model):
    parent = models.ForeignKey("Account", related_name="children", on_delete=models.CASCADE, blank=True, null=True)
    code = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    type = models.IntegerField(choices=account_types)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    def get_code(self):
        code = [self.code, ]
        _parent = self.parent

        while _parent is not None:
            code += [str(_parent.code)]
            _parent = _parent.parent

        code = code[::-1]
        return ''.join(code)


class Transaction(models.Model):
    choices = (
        (1, "بدهکار"),
        (2, "بستانکار")
    )

    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    type = models.IntegerField(choices=choices)
    account_document = models.ForeignKey("AccountingDocument", on_delete=models.CASCADE, related_name="transactions")


class AccountingDocument(models.Model):
    number = models.PositiveIntegerField()
    date_time = jmodels.jDateTimeField()
    description = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT, related_name="documents", null=True, blank=True)

    def __str__(self):
        return str(self.number)




