from django.db import models
from django_jalali.db import models as jmodels
from user_management.models import UserProfile


# Create your models here.


class Account(models.Model):
    parent = models.ForeignKey("Account", related_name="children", on_delete=models.CASCADE, blank=True, null=True)
    code = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

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
    type = models.IntegerField(choices=choices, null=True)
    accountDocument = models.ForeignKey("AccountingDocument", on_delete=models.CASCADE, related_name="transaction")


class AccountingDocument(models.Model):
    number = models.PositiveIntegerField()
    dateTime = jmodels.jDateTimeField()
    description = models.CharField(max_length=255)
    prepared = models.ForeignKey(UserProfile, on_delete=models.PROTECT, related_name="prepared")
    confirmed = models.ForeignKey(UserProfile, on_delete=models.PROTECT, related_name="confirmed")
    approved = models.ForeignKey(UserProfile, on_delete=models.PROTECT, related_name="approved")


    def sum_transations(self):
        transactions = self.transaction.all()
        sum = 0
        for transaction in transactions:
            sum += transaction.amount
        return sum

    def __str__(self):
        return str(self.number)

