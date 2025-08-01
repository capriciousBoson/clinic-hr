from django.db import models
from django.conf import settings
from encrypted_model_fields.fields import EncryptedCharField


class Party(models.Model):

    choice_gender = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]
    
    choice_marital = [
        ("single", "Single"),
        ("married", "Married"),
        ("divorced", "Divorced"),
    ]

    choice_state = [
        ('AL', 'Alabama'), 
        ('AZ', 'Arizona'), 
        ('AR', 'Arkansas'), 
        ('CA', 'California'), 
        ('CO', 'Colorado'), 
        ('CT', 'Connecticut'), 
        ('DE', 'Delaware'), 
        ('DC', 'District of Columbia'), 
        ('FL', 'Florida'), 
        ('GA', 'Georgia'), 
        ('ID', 'Idaho'), 
        ('IL', 'Illinois'), 
        ('IN', 'Indiana'), 
        ('IA', 'Iowa'), 
        ('KS', 'Kansas'), 
        ('KY', 'Kentucky'), 
        ('LA', 'Louisiana'), 
        ('ME', 'Maine'), 
        ('MD', 'Maryland'), 
        ('MA', 'Massachusetts'), 
        ('MI', 'Michigan'), 
        ('MN', 'Minnesota'), 
        ('MS', 'Mississippi'), 
        ('MO', 'Missouri'), 
        ('MT', 'Montana'), 
        ('NE', 'Nebraska'), 
        ('NV', 'Nevada'), 
        ('NH', 'New Hampshire'), 
        ('NJ', 'New Jersey'), 
        ('NM', 'New Mexico'), 
        ('NY', 'New York'), 
        ('NC', 'North Carolina'), 
        ('ND', 'North Dakota'), 
        ('OH', 'Ohio'), 
        ('OK', 'Oklahoma'), 
        ('OR', 'Oregon'), 
        ('PA', 'Pennsylvania'),
        ('RI', 'Rhode Island'), 
        ('SC', 'South Carolina'), 
        ('SD', 'South Dakota'), 
        ('TN', 'Tennessee'), 
        ('TX', 'Texas'), 
        ('UT', 'Utah'), 
        ('VT', 'Vermont'), 
        ('VA', 'Virginia'), 
        ('WA', 'Washington'), 
        ('WV', 'West Virginia'), 
        ('WI', 'Wisconsin'), 
        ('WY', 'Wyoming')
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    ssn = EncryptedCharField(max_length=11) 
    address_full = models.TextField(max_length=128)
    address_city = models.CharField(max_length=50)
    address_zip = models.CharField(max_length=5)
    address_state = models.CharField(max_length=2) 

    marital_status = models.CharField(
        max_length=8,
        choices=choice_marital,
        default="single"
    )

    phone_number = models.CharField(max_length=10)
    email = models.EmailField(max_length=128)

    active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    dependants = models.SmallIntegerField(default=0)

class Employee(models.Model):
    # Employment info
    choice_compensation = [
        ("hourly", "Hourly"),
        ("salaried", "Salaried")
    ]
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    date_hired = models.DateField()
    date_offboarded = models.DateField(null=True, blank=True)

class Contractor(models.Model):
    profile = models.ForeignKey(Party, on_delete=models.CASCADE)
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    contract_start_date = models.DateField()
    contract_end_date = models.DateField()

class Document(models.Model):
    owner = models.ForeignKey(Party, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=64)
    document_name = models.CharField(max_length=128)
    version = models.PositiveIntegerField(default=1)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='uploaded_documents'
        )
    
    expiry_date = models.DateField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True, 
        related_name='deleted_documents')
