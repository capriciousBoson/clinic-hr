from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import Party, EmployeeProfile, ContractorProfile, Document
from django.db import transaction
from datetime import date, timedelta
import re


phone_validator = RegexValidator(
regex=r'^\d{10}$',
message="Phone number must be exactly 10 digits."
)

zip_validator = RegexValidator(
    regex=r'^\d{5}$',
    message="ZIP code must be exactly 5 digits."
)


class  BasePartySerializer(serializers.ModelSerializer):

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
            'first_name', 'last_name', 'dob', 'gender', 'ssn',
            'address_full', 'address_city', 'address_zip', 'address_state',
            'marital_status', 'phone_number', 'email', 'dependants'
        ]
        extra_kwargs = {
            'first_name': {
                'required': True,
                'allow_blank': False,
                # 'min_length': 2,
                # 'max_length': 100
            },
            'last_name': {
                'required': True,
                'allow_blank': False,
                # 'min_length': 2,
                # 'max_length': 100
            },
            'dob' : {
                'required': True,
            },
            'gender' : {
                # 'min_length': 4,
                # 'max_length': 6,
                'required': True,
                'allow_blank': False,
            },
            'marital_status' : {
                # 'min_length': 6,
                # 'max_length': 8,
                'required': True,
                'allow_blank': False,
            },
            'ssn': {
                'write_only': True,
                'required': True,
                'style': {'input_type': 'password'}  # Hide in browsable API,
            },
            'address_full': {
                'required': True,
                'allow_blank': False,
                # 'min_length': 10
            },
            'address_city': {
                'required': True,
                'allow_blank': False,
                # 'min_length': 2
            },
            'address_zip': {
                'required': True,
                'validators': [zip_validator]
            },
            'phone_number': {
                'required': True,
                'validators': [phone_validator]
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
            'first_name', 'last_name', 'dob', 'gender',
            'address_full', 'address_city', 'address_zip', 'address_state',
            'marital_status', 'phone_number', 'email', 'dependants', 'active'
        ]
        extra_kwargs = {
            # 'first_name': {'min_length': 2},
            # 'last_name': {'min_length': 2},
            # 'address_full': {'min_length': 10},
            # 'address_city': {'min_length': 2},
            # 'address_state': {'min_length':2},
            'address_zip': {'validators': [zip_validator]},
            'phone_number': {'validators': [phone_validator]},
        }

class PartyListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing parties"""
    ssn_masked = serializers.SerializerMethodField()


    class Meta:
        model = Party
        fields = [
            'first_name', 'last_name', 'dob', 'gender', 'ssn_masked',
            'address_full', 'address_city', 'address_zip', 'address_state',
            'marital_status', 'phone_number', 'email', 'dependants'
        ]

    def get_ssn_masked(self, obj):
        """Return masked SSN for display"""
        if obj.ssn:
            return f"***-**-{obj.ssn[-4:]}"
        return None
    
# ===================== EMPLOYEE PROFILE SERIALIZERS ===================== #

class EmployeeProfileCreateSerializer(serializers.ModelSerializer):
    """Create Employee with nested Party"""
    
    party = PartyCreateSerializer()
    class Meta:
        model = EmployeeProfile
        fields = [
            'party', 'employer', 'compensation_type',
            'date_hired', 'date_offboarded'
        ]
        extra_kwargs = {
            'employer':{'read_only':True},
            'date_hired': {'required': True},
            'compensation_type':{'required':True},
        }
    
    def validate_date_hired(self, value):
        """Validate hire date"""
        if value > date.today():
            raise serializers.ValidationError("Hire date cannot be in the future.")
        return value
    
    def validate_date_offboarded(self, value):
        """Validate offboard date if provided"""
        if value and value > date.today():
            raise serializers.ValidationError("Offboard date cannot be in the future.")
        return value
    
    def validate(self, attrs):
        """Cross-field validation"""
        date_hired = attrs.get('date_hired')
        date_offboarded = attrs.get('date_offboarded')
        
        if date_offboarded and date_hired and date_offboarded <= date_hired:
            raise serializers.ValidationError({
                'date_offboarded': 'Offboard date must be after hire date.'
            })
        
        return attrs
    
    @transaction.atomic
    def create(self, validated_data):
        """Create Employee with nested Party"""
        party_data = validated_data.pop('party')
        
        
        employer = self.context['request'].user
        print(f"found employer in serializer ---- : {employer}")
        
        # Create Party first
        party = Party.objects.create(**party_data)
        
        # Create Employee
        employee = EmployeeProfile.objects.create(party=party,employer=employer, **validated_data)
        
        return employee
    
class EmployeeProfileUpdateSerializer(serializers.ModelSerializer):
    """Update Employee with nested Party updates"""
    
    party = PartyUpdateSerializer()
    
    class Meta:
        model = EmployeeProfile
        fields = ['party', 'compensation_type', 'date_hired', 'date_offboarded']
    
    def validate_date_offboarded(self, value):
        """Validate offboard date"""
        if value and value > date.today():
            raise serializers.ValidationError("Offboard date cannot be in the future.")
        return value
    
    def validate(self, attrs):
        """Cross-field validation"""
        date_hired = attrs.get('date_hired', self.instance.date_hired)
        date_offboarded = attrs.get('date_offboarded')
        
        if date_offboarded and date_hired and date_offboarded <= date_hired:
            raise serializers.ValidationError({
                'date_offboarded': 'Offboard date must be after hire date.'
            })
        
        return attrs
    
    @transaction.atomic
    def update(self, instance, validated_data):
        """Update Employee and nested Party"""
        party_data = validated_data.pop('party', None)
        
        # Update Party if data provided
        if party_data:
            party_serializer = PartyUpdateSerializer(
                instance.party, 
                data=party_data, 
                partial=True
            )
            if party_serializer.is_valid(raise_exception=True):
                party_serializer.save()
        
        # Update Employee
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance

class EmployeeProfileListSerializer(serializers.ModelSerializer):
    """Retrieve Employee with nested Party details"""
    
    party = PartyListSerializer(read_only=True)
    
    class Meta:
        model = EmployeeProfile
        fields = [
            'id', 'party','compensation_type', 'employer', 'date_hired',
            'date_offboarded'
        ]
    

# ===================== CONTRACTOR PROFILE SERIALIZERS ===================== #

class ContractorCreateSerializer(serializers.ModelSerializer):
    """Create Contractor with nested Party"""
    
    party = PartyCreateSerializer()
    
    
    class Meta:
        model = ContractorProfile
        fields = [
            'profile', 'employer', 'contract_start_date',
            'contract_end_date', 
        ]
        extra_kwargs = {
            'employer': {'required': True},
            'contract_start_date': {'required': True},
            'contract_end_date': {'required': True},
        }
    

    
    def validate(self, attrs):
        """Cross-field validation"""
        start_date = attrs.get('contract_start_date')
        end_date = attrs.get('contract_end_date')
        
        if start_date and end_date:
            if end_date <= start_date:
                raise serializers.ValidationError({
                    'contract_end_date': 'Contract end date must be after start date.'
                })
        
        return attrs

    
    @transaction.atomic
    def create(self, validated_data):
        """Create Contractor with nested Party"""
        party_data = validated_data.pop('profile')
        
        # Create Party first
        party = Party.objects.create(**party_data)
        
        # Create Contractor
        contractor = ContractorProfile.objects.create(profile=party, **validated_data)
        
        return contractor


class ContractorListSerializer(serializers.ModelSerializer):
    """Retrieve Contractor with nested Party details"""
    
    party = PartyListSerializer(read_only=True)
    
    class Meta:
        model = ContractorProfile
        fields = [
            'id', 'party', 'employer', 'contract_start_date',
            'contract_end_date',
        ]
    

class ContractorUpdateSerializer(serializers.ModelSerializer):
    """Update Contractor with nested Party updates"""
    
    party = PartyUpdateSerializer()
    
    class Meta:
        model = ContractorProfile
        fields = ['party', 'contract_start_date', 'contract_end_date']
    
    def validate(self, attrs):
        """Cross-field validation"""
        start_date = attrs.get('contract_start_date', self.instance.contract_start_date)
        end_date = attrs.get('contract_end_date', self.instance.contract_end_date)
        
        if start_date and end_date:
            if end_date <= start_date:
                raise serializers.ValidationError({
                    'contract_end_date': 'Contract end date must be after start date.'
                })
        
        return attrs
    
    @transaction.atomic
    def update(self, instance, validated_data):
        """Update Contractor and nested Party"""
        party_data = validated_data.pop('profile', None)
        
        # Update Party if data provided
        if party_data:
            party_serializer = PartyUpdateSerializer(
                instance.party, 
                data=party_data, 
                partial=True
            )
            if party_serializer.is_valid(raise_exception=True):
                party_serializer.save()
        
        # Update Contractor
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance


