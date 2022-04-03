import random
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from reviews.models import Reviews, Titles, User
from api_yamdb.settings import EMAIL_FROM
from .serializers import (
    SendEmailSerializer,
    CommentsSerializer,
    ReviewsSerializer,
    SendTokenSerializer,
)


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
            confirmation_code=confirmation_code,
            is_active=False
        )

        send_mail(
            'Welcome to yamdb',
            f'code: {confirmation_code}',
            EMAIL_FROM,
            [email],
            fail_silently=True,
        )
        return Response(status=status.HTTP_200_OK)


#@csrf_exempt
class SendToren(APIView):

    def post(self, request):
        serializer = SendTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        confirmation_code = serializer.data['confirmation_code']
        try:
            user = User.objects.get(
                username=username,
            )
        except User.DoesNotExist:
            return Response('Error username')
        if confirmation_code != user.confirmation_code:
            return Response('Error code')
        token = RefreshToken.for_user(user).access_token
        user.is_active = True
        user.save()
        return Response(
            f'token: {str(token)}',
            status=status.HTTP_200_OK
        )

class ReviewsViewSet(viewsets.ModelViewSet):
    """Класс для работы с оценками."""

    serializer_class = ReviewsSerializer
    # permission_classes

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        if title and serializer.is_valid:
            review = Reviews.objects.filter(
                title=title, author=self.request.user
            )
            if len(review) == 0:
                serializer.save(author=self.request.user, title=title)
            else:
                raise serializer.ValidationError('Отзыв уже существует')


class CommentsViewSet(viewsets.ModelViewSet):
    """Класс для работы с комментариями."""

    serializer_class = CommentsSerializer
    # permission_classes =

    def get_queryset(self):
        review = get_object_or_404(Reviews, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Reviews, id=review_id, title=title_id)
        if serializer.is_valid:
            serializer.save(author=self.request.user, review=review)

    def perform_destroy(self, instance):
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_update(self, serializer):
        if self.request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer.save()
