from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import json
from .models import BuzinessInformation
from .utility import MpesaClient
from .serializer import BuzinessInformationSerializer
from .fcmPush import sendPushNotification

@api_view(['POST'])
def create_account_view(request):
    serializer = BuzinessInformationSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

b'{"Body":{"stkCallback":{"MerchantRequestID":"91c3-4af9-acf0-8d25ce54c54126515",'
'"CheckoutRequestID":"ws_CO_14042025231938794791315487",'
'"ResultCode":1037,"ResultDesc":"DS timeout user cannot be reached"}}}'
@api_view(['GET', 'POST'])
def stk_push(request):
    if request.method == "POST":
       
        # consumer_key = request.data.get("consumer_key")  
        # consumer_secret = request.data.get("consumer_secret")
        # passKey = request.data.get("passKey")
        phone_number = request.data.get("phone_number")
        amount = request.data.get("amount")
        busines_id = request.data.get("business_id")
        transaction_desc = "business otty"
        business = BuzinessInformation.objects.filter(business_id=busines_id).first()
        if business:
            consumer_key = business.customer_key
            consumer_secret = business.customer_secret
            passKey = business.passKey
            short_code = business.till_number
            business_name = business.business_name
            print(f"{consumer_key},{short_code},{passKey}")
            mpesa = MpesaClient(consumer_key=consumer_key,
                                    consumer_secret=consumer_secret,
                                    shortcode=short_code, passKey=passKey, 
                                    business_id=business.business_id)
            
            response =  mpesa.initiate_payment(amount=amount, 
                                         phone_number=phone_number,
                                         transaction_desc=transaction_desc,
                                         business_name=business_name)
            print(f"response {response}")
            return Response(response)
        else:
           return Response({"message": "invalid account number ensure you registered with the bizfity"})

    return Response({"message": "Send a POST request with STK push details"})

# "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"

{
    "amount":1,
    "phone_number":"254791315487",
    "business_id":"51589cb3-1631-4f4e-9e12-f3242fc93c83"
}

@csrf_exempt
def stk_callback(request,business_id):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)
    print(request.body)

    data = json.loads(request.body)
    business = BuzinessInformation.objects.filter(business_id=business_id).first()
    sendPushNotification(
        device_token= business.device_fcm_token
        ,body="2000 shillings received from john duo"
         ,title="payment received"
        )
    print("STK Callback for Business ID:", business_id)
    
    
    # Process and save transaction here
    
    return JsonResponse({"ResultCode": 0, "ResultDesc": "STK Callback Received"})


def confirmation_view(request, business_id):
    
    print(f"confirmation for {business_id} | {request.body}")
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})


def validation_view(request, business_id):
    
    print(f"confirmation for {business_id} | {request.body}")
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})




