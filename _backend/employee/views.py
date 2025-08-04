from rest_framework.views import APIView
from rest_framework.response import response

class EmployeeView(APIView):
    def post(self, request):
        user = request.user
        

