from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from .models import BuzinessInformation
from .utility import MpesaClient

@receiver(post_save, sender =BuzinessInformation)
def register_mpesa_urls(sender, instance, created, **kwargs):
    base_url ="https://719c-105-163-156-10.ngrok-free.app/"
    if created:
        print(f"new business created {instance.business_name}")
        business_id = instance.business_id
        customer_secret = instance.customer_secret
        customer_key = instance.customer_key
        till_number = instance.till_number
        passKey = instance.passKey


        mpesaClient = MpesaClient(business_id= business_id,
                                consumer_secret=customer_secret,
                                consumer_key=customer_key,
                                passKey=passKey,
                                shortcode=till_number
                                )
        access_token = mpesaClient.get_access_token()
        print(f"token {access_token}")
        url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
        headers = {
         'Content-Type': 'application/json',
         'Authorization': f'Bearer {access_token}'
        }

        payload = {
                "ShortCode": till_number,
                 "ResponseType": "Completed",
                "ConfirmationURL": f"{base_url}api/confirmation/{business_id}",
                "ValidationURL": f"{base_url}api/validation/{business_id}",
          }
        print(f"payload {payload} ")

        response = requests.post(url, headers = headers, data = payload)
        print(response.text)

