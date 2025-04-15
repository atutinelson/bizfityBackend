from rest_framework import serializers
from .models import BuzinessInformation,MpesaToken
import re

class BuzinessInformationSerializer(serializers.ModelSerializer):

    def validate_contact(self, value):
        pattern = r'^(07\d{8}|2547\d{8}|\+2547\d{8})$'
        if re.match(pattern, value):
            raise serializers.ValidationError(
                "Enter a valid Kenyan phone number (e.g., 0712345678 or +254712345678)."
            )
        return value
    
    def validate_business_name(self, value):
        if BuzinessInformation.objects.filter(business_name__iexact = value).exists():
            raise serializers.ValidationError(
                "Business name already exists."
            )
        return value
        
    def validate_till_number(self, value):
        if value:
            if not value.isdigit():
                raise serializers.ValidationError("Till number must be numeric.")
            if not (5 <= len(value) <= 7):
                raise serializers.ValidationError("Till number must be between 5 and 7 digits.")
        return value
    
    class Meta:
        model = BuzinessInformation
        fields = [
            'business_id',
            'business_name',
            'business_address',
            'email',
            'contact',
            'till_number',
            'pay_bill',
            'device_fcm_token',
            'customer_key',
            'customer_secret',
            'passKey'
        ]




class MpesaTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaToken
        fields =[
            "token",
            "business",
            "expire_at"
        ]