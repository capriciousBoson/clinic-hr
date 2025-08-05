from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import EmployeeProfile
from .serializers import (
                EmployeeProfileCreateSerializer,
                EmployeeProfileListSerializer,
                EmployeeProfileUpdateSerializer,
                ContractorCreateSerializer,
                ContractorListSerializer,
                ContractorUpdateSerializer)

class EmployeeProfileListCreateView(APIView):
    def get(self, request):
        employee_profiles = EmployeeProfile.objects.all()
        serializer = EmployeeProfileListSerializer(employee_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = EmployeeProfileCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    
class EmployeeProfileDetailView(APIView):
    def get(self, request, id):
        employee_profile = get_object_or_404(EmployeeProfile, id=id)
        serializer = EmployeeProfileListSerializer(employee_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        employee_profile = get_object_or_404(EmployeeProfile, id=id)
        serializer = EmployeeProfileUpdateSerializer(employee_profile, 
                                                     data=request.data,
                                                     partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


