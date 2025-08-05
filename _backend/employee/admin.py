from django.contrib import admin
from .models import Party, EmployeeProfile, ContractorProfile, Document

admin.site.register(Party)
admin.site.register(EmployeeProfile)
admin.site.register(ContractorProfile)
admin.site.register(Document)