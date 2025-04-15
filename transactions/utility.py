
import requests
from requests.auth import HTTPBasicAuth
import base64
import json
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.timezone import localtime
from .models import MpesaToken, BuzinessInformation
from .serializer import MpesaTokenSerializer

class MpesaClient:
    def __init__(self, consumer_key, consumer_secret, shortcode, passKey, business_id):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.passKey = passKey
        self.shortcode = shortcode
        self.business_id = business_id
        self.base_url = "https://sandbox.safaricom.co.ke"

    def get_access_token(self):
        url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        business = BuzinessInformation.objects.filter(business_id =self.business_id).first()
        token = MpesaToken.objects.filter(business=business).first()
            
        if token==None or timezone.now()  >= token.expire_at:
            print("regenarating token")
            response = requests.get(url, auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret))
            expiry_time = localtime(timezone.now() + timedelta(seconds=int(response.json()['expires_in'])))
            print(f"current time {localtime(timezone.now())}")
            access_token = response.json()["access_token"]
            
            if  token:
                token.expire_at =expiry_time
                token.token = access_token

            else:
                MpesaToken.objects.create(
                    business=business,
                    token=access_token,
                    expire_at = expiry_time
                )
            
            
            return access_token
        else:
            print(f"token {token.token}")
            return token.token
            
            
        
        
  
        

  
    def initiate_payment(self, phone_number, amount, transaction_desc, business_name):
        urlPath = f"{self.base_url}/mpesa/stkpush/v1/processrequest"
        access_token = self.get_access_token()
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode((self.shortcode + self.passKey+ timestamp).encode()).decode()

        headers = {
         'Content-Type': 'application/json',
         'Authorization': f'Bearer {access_token}'
        }

        payload = {
         "BusinessShortCode": self.shortcode,
          "Password":  password,
          "Timestamp": timestamp,
           "TransactionType": "CustomerPayBillOnline",
           "Amount": amount,
           "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
           "CallBackURL": f"https://68b3-105-163-158-229.ngrok-free.app/api/stk_callback/{self.business_id}/",
           "AccountReference": f"Bizfity {business_name}",
          "TransactionDesc": transaction_desc 
          }

        response = requests.post(url=urlPath,headers = headers, json= payload)
        return response.json()


def registerConfirmationUrl():
    url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {
      'Content-Type': 'application/json',
     'Authorization': 'Bearer COpJouagui5jAehJv9eQFZZwphKG'
      }

    payload = {
      "ShortCode": 600426,
      "ResponseType": "Completed",
      "ConfirmationURL": "https://mydomain.com/confirmation",
      "ValidationURL": "https://mydomain.com/validation",
    }

    response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl', headers = headers, data = payload)
    print(response.text.encode('utf8'))