from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import Party, EmployeeProfile, ContractorProfile, Document
from django.db import transaction
from django.db.models import Max
from datetime import date, timedelta
from pathlib import Path
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
    

    def validate_phone_number(self, value):
        if self.instance:
            # For updates, exclude current instance
            if Party.objects.filter(phone_number=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("Phone number already exists.")
        else:
            # For creation
            if Party.objects.filter(phone_number=value).exists():
                raise serializers.ValidationError("Phone number address already exists.")
        
        return value.lower()




class PartyCreateSerializer(BasePartySerializer):
    """Serializer for creating new Party instances"""
    
    class Meta:
        model = Party
        fields = [
            "email", "phone_number", "address_full", "address_city",
            "address_zip", "address_state", "active"
        ]
        extra_kwargs = {
            "phone_number": {"validators": [phone_validator]},
            "address_zip": {"validators": [zip_validator], "required": False},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True}
        }
    
class PartyUpdateSerializer(BasePartySerializer):
    """Serializer for updating Party instances (excludes SSN)"""
    
    class Meta:
        model = Party
        fields = [
            "email", "phone_number", "address_full", "address_city",
            "address_zip", "address_state", "active"
        ]
        extra_kwargs = {
            "phone_number": {"validators": [phone_validator]},
            "address_zip": {"validators": [zip_validator], "required": False},
        }
    def validate_email(self, value):
        """Custom validation for email uniqueness"""
        if self.instance and self.instance.email == value:
            # If the email hasn't changed, skip uniqueness validation
            return value
        
        # Check if email already exists for other instances
        if Party.objects.filter(email=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("A party with this email already exists.---")
        
        return value
    
    def validate_phone_number(self, value):
        """Custom validation for phone number uniqueness"""
        # First run the phone validator
        # print(f"debug----  instance : {self.instance}, value : {value}")
        phone_validator(value)
        # print(f"validating phone_number - {self.instance.phone_number, value}")
        if self.instance and self.instance.phone_number == value:
            # If the phone number hasn't changed, skip uniqueness validation
            return value
        
        # Check if phone number already exists for other instances
        if Party.objects.filter(phone_number=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("A party with this phone number already exists.---")
        
        return value

class PartyListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing parties"""
    class Meta:
        model = Party
        fields = [
            "id", "email", "phone_number", "address_full",
            "address_city", "address_zip", "address_state", "active"
        ]
    
# ===================== EMPLOYEE PROFILE SERIALIZERS ===================== #

class EmployeeProfileCreateSerializer(serializers.ModelSerializer):
    """Create Employee with nested Party"""
    
    party = PartyCreateSerializer(write_only=True, required=True)
    class Meta:
        model = EmployeeProfile
        fields = [
            "party",
            "employer", "first_name", "last_name", "dob", "gender",
            "ssn", "marital_status", "dependants", "compensation_type",
            "date_hired", "date_offboarded"
        ]
        extra_kwargs = {
            "employer": {"read_only": True},
            "ssn": {"style": {"input_type": "password"}},
            "date_hired": {"required": False},
        }
    

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
        
        employee = EmployeeProfile.objects.create(
                                                employer=employer,
                                                **party_data,
                                                **validated_data
                                            )
        return employee
    
class EmployeeProfileUpdateSerializer(serializers.ModelSerializer):
    """Update Employee with nested Party updates"""
    
    party = PartyUpdateSerializer(source='*', read_only=True)
    class Meta:
        model = EmployeeProfile
        fields = [
            "party", "first_name", "last_name", "dob", "gender",
            "ssn", "marital_status", "dependants", "compensation_type",
            "date_hired", "date_offboarded"
        ]
    
    
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
                instance=instance, 
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
        
        # return super().update(instance, validated_data)

class EmployeeProfileListSerializer(serializers.ModelSerializer):
    """Retrieve Employee with nested Party details"""
    
    party = PartyListSerializer(source='*', read_only=True)
    
    class Meta:
        model = EmployeeProfile
        fields = [
            "id","party", "first_name", "last_name", "dob", "gender",
            "ssn", "marital_status", "dependants", "compensation_type",
            "date_hired", "date_offboarded"
        ]
    

# ===================== CONTRACTOR PROFILE SERIALIZERS ===================== #

class ContractorProfileCreateSerializer(serializers.ModelSerializer):
    """Create Contractor with nested Party"""
    
    party = PartyCreateSerializer(write_only=True, required=True)
    
    class Meta:
        model = ContractorProfile
        fields = ["id", "party", "employer", "contractor_name", "tin"]

        extra_kwargs = {
            "employer": {"read_only": True},
            "tin": {"style": {"input_type": "password"}}
        }

    
    @transaction.atomic
    def create(self, validated_data):
        """Create Contractor with nested Party"""
        party_data = validated_data.pop('party')
        

        employer = self.context['request'].user
        
        # Create Contractor
        contractor = ContractorProfile.objects.create(
                                    employer=employer,
                                    **party_data,
                                    **validated_data)
        
        return contractor


class ContractorProfileListSerializer(serializers.ModelSerializer):
    """Retrieve Contractor with nested Party details"""
    
    party = PartyListSerializer(source='*', read_only=True)
    
    class Meta:
        model = ContractorProfile
        fields = ["id", "party", "employer", "contractor_name", "tin"]
    

class ContractorProfileUpdateSerializer(serializers.ModelSerializer):
    """Update Contractor with nested Party updates"""
    
    party = PartyUpdateSerializer(source='*', read_only=True)
    class Meta:
        model = ContractorProfile
        fields = ["party", "contractor_name", "tin"]
    

    
    @transaction.atomic
    def update(self, instance, validated_data):
        """Update Contractor and nested Party"""
        party_data = validated_data.pop('party', None)
        # print(f"this is the party data in contractor update serializer - {party_data}------------")
        
        # Update Party if data provided
        if party_data:
            party_serializer = PartyUpdateSerializer(
                instance=instance, 
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
    
# class DocumentCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Document
#         fields = [
#             'party', 'document_type', 'document_name',
#             'contract_end_date', 
#         ]


# ===================== DOCUMENT SERIALIZERS ===================== #
ALLOWED_EXTS = {".pdf", ".png", ".jpg", ".jpeg", ".doc", ".docx"}
MAX_BYTES = 10 * 1024 * 1024  # 10 MB

def validate_upload(file):
    # Size
    if file.size > MAX_BYTES:
        raise serializers.ValidationError(f"File too large. Max is {MAX_BYTES // (1024*1024)} MB.")
    # Extension (fallback if content_type is unreliable)
    ext = Path(file.name).suffix.lower()
    if ext not in ALLOWED_EXTS:
        raise serializers.ValidationError(
            f"Unsupported file type '{ext}'. Allowed: {', '.join(sorted(ALLOWED_EXTS))}"
        )


def next_version_for(doc: Document) -> int:
    """Compute next version number for the (party, document_type, document_name) group."""
    qs = Document.objects.filter(
        party=doc.party,
        document_type=doc.document_type,
        document_name=doc.document_name,
    )
    current_max = qs.aggregate(m=Max("version"))["m"]
    return (current_max or 0) + 1


class DocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            "id",
            "party",
            "document_type",
            "document_name",
            "document",
            "version",
            "expiry_date",
            "uploaded_at",
            "uploaded_by",
        ]
        read_only_fields = ["id", "version", "uploaded_at", "uploaded_by"]

    def validate_document(self, file):
        validate_upload(file)
        return file

    def create(self, validated_data):
        upload = validated_data.pop("document")

        # Stamp who uploaded
        user = self.context.get("request").user if self.context.get("request") else None
        if user and user.is_authenticated:
            validated_data["uploaded_by"] = user
        
        temp = Document(**validated_data)
        temp.version = next_version_for(temp)
        temp.document = None
        temp.save()  

        # Build final path with party_id + pk + versioned filename
        final_path = temp.build_final_document_path(upload.name)

        # Auto version (only if not explicitly provided—which it isn't by default)
        # Construct a temporary Document-like object for grouping
        # Save file into the final path
        storage = temp.document.storage  # respects DEFAULT_FILE_STORAGE
        saved_name = storage.save(final_path, upload)
        temp.document.name = saved_name
        temp.save(update_fields=["document"])

        return temp

class DocumentUpdateSerializer(serializers.ModelSerializer):
    # Prevent changing party via serializer-level write-protection
    party = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Document
        fields = [
            "id",
            "party",
            "document_type",
            "document_name",
            "document",
            "version",
            "expiry_date",
            "deleted_at",
            "deleted_by",
            "uploaded_at",
            "uploaded_by",
        ]
        read_only_fields = [
            "id",
            "version",
            "uploaded_at",
            "uploaded_by",
            "deleted_by",
        ]

    def validate_document(self, file):
        # Only validate if a new file was provided
        if file is not None:
            validate_upload(file)
        return file

    def update(self, instance, validated_data):
        upload = validated_data.pop("document", None)

        # If a new file is provided, bump version and re-save to a new versioned path
        if upload is not None:
            instance.version = instance.version + 1
            # Save instance to persist version bump (no file yet)
            instance.save(update_fields=["version"])

            final_path = instance.build_final_document_path(upload.name)
            storage = instance.document.storage
            saved_name = storage.save(final_path, upload)
            instance.document.name = saved_name

        # Handle soft-delete stamping (optional)
        if "deleted_at" in validated_data and validated_data["deleted_at"] and not instance.deleted_by:
            user = self.context.get("request").user if self.context.get("request") else None
            if user and user.is_authenticated:
                instance.deleted_by = user

        # Update non-file fields
        for k, v in validated_data.items():
            setattr(instance, k, v)

        instance.save()
        return instance
    
class DocumentListSerializer(serializers.ModelSerializer):
    document_url = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()
    days_to_expiry = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            "id",
            "party",
            "document_type",
            "document_name",
            "version",
            "document_url",
            "uploaded_at",
            "uploaded_by",
            "expiry_date",
            "is_expired",
            "days_to_expiry",
            "deleted_at",
            "deleted_by",
        ]
        read_only_fields = fields  # fully read-only in list/detail views

    def get_document_url(self, obj: Document):
        # Build absolute URL if request is present
        request = self.context.get("request")
        if hasattr(obj.document, "url"):
            url = obj.document.url
            return request.build_absolute_uri(url) if request else url
        return None

    def get_is_expired(self, obj: Document):
        return bool(obj.expiry_date and obj.expiry_date < date.today())

    def get_days_to_expiry(self, obj: Document):
        if not obj.expiry_date:
            return None
        return (obj.expiry_date - date.today()).days