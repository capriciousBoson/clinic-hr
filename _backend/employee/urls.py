from django.urls import path
from .views import (
                EmployeeProfileListCreateView, 
                EmployeeProfileDetailView, 
                ContractorProfileListCreateView, 
                ContractorProfileDetailView,
                DocumentListCreateView,
                DocumentDetailView)

urlpatterns = [
    path('employeeapi/', EmployeeProfileListCreateView.as_view(), name='employee-list-create'),
    path('employeeapi/<int:id>/', EmployeeProfileDetailView.as_view(), name='employee-detail'),
    path('contractorapi/', ContractorProfileListCreateView.as_view(), name='Contractor-list-create'),
    path('contractorapi/<int:id>/', ContractorProfileDetailView.as_view(), name='contractor-detail'),
    path('documentapi/', DocumentListCreateView.as_view(), name='document-list-create'),
    path('documentapi/<int:id>/',DocumentDetailView.as_view(), name='document-detail')

]
