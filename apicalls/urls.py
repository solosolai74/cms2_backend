from django.urls import path
from apicalls.otp import PXEOTPGEN,CustomAuthToken

urlpatterns = [
    path('pxeotpgen/', PXEOTPGEN.as_view(), name='pxeotpgen'),
    path('api-token-auth/',CustomAuthToken.as_view(), name='api_token_auth'),
]