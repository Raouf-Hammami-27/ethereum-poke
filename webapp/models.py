from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    name = models.CharField(blank=True, max_length=255)
    address = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return self.username


class Transaction(models.Model):

    txHash = models.CharField(max_length=100)
    timeStamp = models.DateField(blank=True, default=datetime.now())
    fr = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name="transactions")
    contract_address = models.CharField(max_length=42)
    gasUsedByTxn = models.FloatField(null=True)

    def __str__(self):
        return 'address {}'.format(self.fr, self.timeStamp)