from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import Party, EmployeeProfile, ContractorProfile, Document
from datetime import date, timedelta
import re




class  BasePartySerializer(serializers.ModelSerializer):
    phone_validator = RegexValidator(
    regex=r'^\d{10}$',
    message="Phone number must be exactly 10 digits."
    )

    zip_validator = RegexValidator(
        regex=r'^\d{5}$',
        message="ZIP code must be exactly 5 digits."
    )

    # Custom validation methods
    def validate_dob(self, value):
        """Validate date of birth"""
        today = date.today()
        min_age_date = today - timedelta(days=365 * 120)  # 120 years max
        max_age_date = today - timedelta(days=365 * 18)   # 18 years min
        
        if value > today:
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        if value < min_age_date:
            raise serializers.ValidationError("Invalid date of birth.")
        if value > max_age_date:
            raise serializers.ValidationError("Must be at least 18 years old.")
        
        return value
    
    def validate_email(self, value):
        """Custom email validation"""
        # Check for unique email (if needed)
        if self.instance:
            # For updates, exclude current instance
            if Party.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("Email address already exists.")
        else:
            # For creation
            if Party.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email address already exists.")
        
        return value.lower()  # Normalize to lowercase
    
    def validate_dependants(self, value):
        """Validate dependants count"""
        if value < 0:
            raise serializers.ValidationError("Dependants cannot be negative.")
        if value > 20:  # Reasonable upper limit
            raise serializers.ValidationError("Dependants count seems unusually high.")
        return value
    def validate_ssn(self, value):
        """Validate SSN format and uniqueness"""
        # Remove any formatting
        ssn_digits = re.sub(r'\D', '', value)
        
        if len(ssn_digits) != 9:
            raise serializers.ValidationError("SSN must be exactly 9 digits.")
        
        # Check for obviously invalid SSNs
        invalid_ssns = ['000000000', '123456789', '111111111', '222222222']
        if ssn_digits in invalid_ssns:
            raise serializers.ValidationError("Invalid SSN format.")
        
        # Check uniqueness
        if Party.objects.filter(ssn=ssn_digits).exists():
            raise serializers.ValidationError("SSN already exists.")
        
        return ssn_digits



class PartyCreateSerializer(BasePartySerializer):
    """Serializer for creating new Party instances"""
    
    class Meta:
        model = Party
        fields = [
            'first_name', 'last_name', 'dob', 'ssn',
            'address_full', 'address_city', 'address_zip', 'address_state',
            'marital_status', 'phone_number', 'email', 'dependants'
        ]
        extra_kwargs = {
            'first_name': {
                'required': True,
                'allow_blank': False,
                'min_length': 2,
                'max_length': 100
            },
            'last_name': {
                'required': True,
                'allow_blank': False,
                'min_length': 2,
                'max_length': 100
            },
            'ssn': {
                'write_only': True,
                'required': True,
                'style': {'input_type': 'password'}  # Hide in browsable API,
            },
            'address_full': {
                'required': True,
                'allow_blank': False,
                'min_length': 10
            },
            'address_city': {
                'required': True,
                'allow_blank': False,
                'min_length': 2
            },
            'address_zip': {
                'required': True,
                'validators': [BasePartySerializer.zip_validator]
            },
            'phone_number': {
                'required': True,
                'validators': [BasePartySerializer.phone_validator]
            },
            'email': {
                'required': True,
                'allow_blank': False
            }
        }
    
class PartyUpdateSerializer(BasePartySerializer):
    """Serializer for updating Party instances (excludes SSN)"""
    
    class Meta:
        model = Party
        fields = [
            'first_name', 'last_name', 'dob',
            'address_full', 'address_city', 'address_zip', 'address_state',
            'marital_status', 'phone_number', 'email', 'dependants', 'active'
        ]
        extra_kwargs = {
            'first_name': {'min_length': 2},
            'last_name': {'min_length': 2},
            'address_full': {'min_length': 10},
            'address_city': {'min_length': 2},
            'address_state': {'min_length':2},
            'address_zip': {'validators': [BasePartySerializer.zip_validator]},
            'phone_number': {'validators': [BasePartySerializer.phone_validator]},
        }
class PartyListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing parties"""
    ssn_masked = serializers.SerializerMethodField()


    class Meta:
        model = Party
        fields = [
            'first_name', 'last_name', 'dob', 'ssn_masked',
            'address_full', 'address_city', 'address_zip', 'address_state',
            'marital_status', 'phone_number', 'email', 'dependants'
        ]

    def get_ssn_masked(self, obj):
        """Return masked SSN for display"""
        if obj.ssn:
            return f"***-**-{obj.ssn[-4:]}"
        return None
    
