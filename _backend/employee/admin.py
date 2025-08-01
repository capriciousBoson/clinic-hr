from django.contrib import admin
from .models import Party, Employee, Contractor, Document

admin.site.register(Party)
admin.site.register(Employee)
admin.site.register(Contractor)
admin.site.register(Document)