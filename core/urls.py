"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from dj_rest_auth.views import PasswordResetConfirmView
from dj_rest_auth.registration.views import VerifyEmailView,ConfirmEmailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/account/',include('apps.accounts.api.urls',namespace='account')),
    path('api/v1/auth/', include('dj_rest_auth.urls')),
    path('api/v1/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/v1/auth/password/reset/confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(),name='password_reset_confirm'),

    path('api/v1/auth/registration/verify-email/',VerifyEmailView.as_view(), name='rest_verify_email'),
    path('api/v1/auth/registration/account-confirm-email/',VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$',VerifyEmailView.as_view(), name='account_confirm_email'),
    path('api/v1/auth/registration/account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
    
    path('api/v1/post/', include('apps.post.api.urls',namespace='post')),
    path('api/v1/comment/', include('apps.comment.api.urls',namespace='comment')),
]
