import random
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from reviews.models import User
from api_yamdb.settings import EMAIL_FROM
from .serializers import SendEmailSerializer


class Registration(APIView):

    def post(self, request):
        serializer = SendEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data['email']
        username = serializer.data['username']
        confirmation_code = random.randint(1111, 9999)
        User.objects.get_or_create(
            email=email,
            username=username,
            confirmation_code=confirmation_code
        )

        send_mail(
            'Welcome to yamdb',
            f'code: {confirmation_code}',
            EMAIL_FROM,
            [email],
            fail_silently=True
        )
        return Response(status=status.HTTP_200_OK)


def send_token(request):
    pass
