from django.urls import path

from apps.users.views.devices import UserDeviceListCreateAPIView, UserDeviceDestroyAPIView
from apps.users.views.register import LoginAPIView, MeAPIView, ProfileUpdateAPIView, RegisterAPIView, ResendVerificationCodeAPIView, SetPasswordAPIView, UpdatePasswordAPIView, UpdatePhoneAPIView, VerifyCodeAPIView, VerifyUpdateCodeAPIView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('verify/', VerifyCodeAPIView.as_view(), name='verify'),
    path('resend-code/', ResendVerificationCodeAPIView.as_view(), name='resend-code'),
    path('set-password/', SetPasswordAPIView.as_view(), name='set-password'),
    path('update-password/', UpdatePasswordAPIView.as_view(), name='update-password'),
    path('me/', MeAPIView.as_view(), name='me'),
    path('update-phone/', UpdatePhoneAPIView.as_view(), name='update-phone'),
    path('verify-update-code/', VerifyUpdateCodeAPIView.as_view(), name='verify-update-code'),
    path('profile/', ProfileUpdateAPIView.as_view(), name='profile'),

    path('devices/', UserDeviceListCreateAPIView.as_view(), name='list-create-devices'),
    path('devices/<str:device_id>/', UserDeviceDestroyAPIView.as_view(), name='delete-device'),
]