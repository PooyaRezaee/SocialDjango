from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView


app_name = 'account'

urlpatterns = [
    path('test/',TestAPI.as_view(),name="test-iauth"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileAPIView.as_view(), name='profile_image'),
    path('profile/picture/', ProfilePictureAPIView.as_view(), name='profile_image'),
    path('profile/picture/<str:username>/', SeeProfilePictureAPIView.as_view(), name='set_profile_image')
]