from rest_framework.response import Response
from rest_framework import status


class PrivetAccountRequired:
    def dispatch(self, request, *args, **kwargs):
        if request.user.private_account:
            return super().dispatch(request, *args, **kwargs)
        else:
            return Response({'detail':"You'r account not privet"},status=status.HTTP_400_BAD_REQUEST)
