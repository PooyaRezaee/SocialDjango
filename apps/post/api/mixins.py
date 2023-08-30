from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from apps.accounts.models import User
from apps.accounts.permisions import IsFollowerOrSelfPermissions


class ForPrivetPageFollowingRequired:
    def get(self, request, username, *args, **kwargs):
        user_request = request.user
        try:
            user_target = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return Response({"detail": "User Doesn't exist."}, status=status.HTTP_404_NOT_FOUND)

        if user_target.private_account:
            is_follower = IsFollowerOrSelfPermissions(user_request, user_target)
            if not is_follower:
                return Response({"detail": "You must be a follower of this account."}, status=status.HTTP_403_FORBIDDEN)

        return super().get(request, *args, **kwargs)
