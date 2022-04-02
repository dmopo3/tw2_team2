from django.urls import path
from .views import Registration, send_token


urlpatterns = [
    path('v1/auth/signup/', Registration.as_view()),
    path('v1/auth/token/', send_token),
]
