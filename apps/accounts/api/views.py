from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

__all__ = [
    'TestAPI',
]

class TestAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        return Response({'status':'OK'})