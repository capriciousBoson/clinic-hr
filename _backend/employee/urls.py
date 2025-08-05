from django.urls import path
from .views import EmployeeProfileListCreateView, EmployeeProfileDetailView

urlpatterns = [
    path('employeeapi/', EmployeeProfileListCreateView.as_view(), name='employee-list-create'),
    path('employeeapi/<int:id>/', EmployeeProfileDetailView.as_view(), name='employee-detail'),
]
