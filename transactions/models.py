from django.db import models
import uuid
from datetime import datetime

class BuzinessInformation(models.Model):
    business_id = models.CharField(default=uuid.uuid4, unique=True, editable=False)
    business_name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    contact = models.CharField(max_length=20)
    till_number = models.CharField(max_length=20, null=True, blank=True)
    business_address = models.CharField(max_length=100, null=True, blank=True)
    pay_bill = models.CharField(max_length=20, null=True, blank=True)
    device_fcm_token = models.CharField(max_length=500)
    customer_secret = models.CharField(max_length=100)
    customer_key = models.CharField(max_length=100)
    passKey = models.CharField(max_length=100)


class MpesaToken(models.Model):
    token= models.CharField(max_length=200)
    business = models.ForeignKey(BuzinessInformation,related_name="mpesaAccessToken", on_delete=models.CASCADE)
    expire_at = models.DateTimeField()
