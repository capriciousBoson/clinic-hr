from django.db import models
from django.conf import settings

# Create your models here.
class Employee(models.Model):

    choice_gender = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]
    
    choice_marital = (
        ("single", "Single"),
        ("married", "Married"),
        ("divorced", "Divorced"),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    ssn = models.CharField(max_length=11)  # To be encrypted in production
    address_full = models.TextField()
    address_city = models.CharField(max_length=50)
    address_zip = models.CharField(max_length=5)
    address_state = models.CharField(max_length=2)  # e.g. 'CA', 'NY'

    # Employment info
    is_contractor = models.BooleanField(default=False)
    is_salaried = models.BooleanField(default=False)
    date_hired = models.DateField()
    date_offboarded = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    # Related employer (user)
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Documents
    contract = models.FileField(upload_to='contracts/', null=True, blank=True)
    w4_form = models.FileField(upload_to='w4_forms/', null=True, blank=True)
    credentials = models.FileField(upload_to='credentials/', null=True, blank=True)
    work_auth_docs = models.FileField(upload_to='work_auth/', null=True, blank=True)