from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.shortcuts import get_object_or_404
from .models import Party, EmployeeProfile, ContractorProfile, Document
from .serializers import (
                EmployeeProfileCreateSerializer,
                EmployeeProfileListSerializer,
                EmployeeProfileUpdateSerializer,
                ContractorProfileCreateSerializer,
                ContractorProfileListSerializer,
                ContractorProfileUpdateSerializer,
                DocumentCreateSerializer,
                DocumentListSerializer,
                DocumentUpdateSerializer)

class EmployeeProfileListCreateView(APIView):
    def get(self, request):
        employee_profiles = EmployeeProfile.objects.all()
        serializer = EmployeeProfileListSerializer(employee_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):

        # print(f"request.data - {request.data}")
        serializer = EmployeeProfileCreateSerializer(data=request.data, context={'request': request})
        # print(f"found user - {request.user}")

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(f"serializer erors - {serializer.errors}")
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
    
class ContractorProfileListCreateView(APIView):
    def get(self, request):
        contractor_profiles = ContractorProfile.objects.all()
        serializer = ContractorProfileListSerializer(contractor_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):

        # print(f"request.data - {request.data}")
        serializer = ContractorProfileCreateSerializer(data=request.data, context={'request': request})
        # print(f"found user - {request.user}")

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(f"serializer errors - {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractorProfileDetailView(APIView):
    def get(self, request, id):
        contractor_profile = get_object_or_404(ContractorProfile, id=id)
        serializer = ContractorProfileListSerializer(contractor_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        contractor_profile = get_object_or_404(ContractorProfile, id=id)
        # print(f"found the following contractor - {contractor_profile}")
        # print(contractor_profile)  # which model is it?
        # print(type(contractor_profile))
        # print(contractor_profile.party_id)  # FK value from Python
        # print(contractor_profile.party)  # will trigger relation fetch
        serializer = ContractorProfileUpdateSerializer(contractor_profile, 
                                                     data=request.data,
                                                     partial=True,
                                                     context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DocumentListCreateView(APIView):
    """
    GET  /api/docs/   -> list ALL documents 
    POST /api/docs/   -> create (multipart supported)
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request):
        party_id = request.query_params.get("party")
        if not party_id:
            return Response({"detail": "Query param 'party' is required, e.g. /api/emp/documentapi/?party=1"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            party_id = int(party_id)
        except (TypeError, ValueError):
            return Response({"detail": "Query param 'party' must be an integer."},
                            status=status.HTTP_400_BAD_REQUEST)
        # Ensure the party exists (gives a clean 404 if not)
        get_object_or_404(Party, pk=party_id)

        docs = Document.objects.filter(party_id=party_id).order_by("-uploaded_at", "-id")
        serializer = DocumentListSerializer(docs, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = DocumentCreateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentDetailView(APIView):
    """
    GET   /api/docs/<id>/   -> retrieve
    PUT   /api/docs/<id>/   -> full update
    PATCH /api/docs/<id>/   -> partial update
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request, id):
        doc = get_object_or_404(Document, pk=id)
        serializer = DocumentListSerializer(doc, context={"request": request})
        return Response(serializer.data)

    def put(self, request, id):
        doc = get_object_or_404(Document, pk=id)
        serializer = DocumentUpdateSerializer(
                                                doc, 
                                                data=request.data, 
                                                context={"request": request},
                                                partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def patch(self, request, pk):
    #     doc = get_object_or_404(Document, pk=pk)
    #     serializer = DocumentUpdateSerializer(doc, data=request.data, partial=True, context={"request": request})
    #     if serializer.is_valid():
    #         instance = serializer.save()
    #         return Response(DocumentListSerializer(instance, context={"request": request}).data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   