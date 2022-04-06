import random
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)

from reviews.models import Reviews, Titles, User, Categories, Genres
from api_yamdb.settings import EMAIL_FROM
from .permissions import (
    IsAdminModeratorOwnerOrReadOnly,
    IsAdminOrReadOnly,
    IsAdmin,
)
from .serializers import (
    SendEmailSerializer,
    CommentsSerializer,
    ReviewsSerializer,
    SendTokenSerializer,
    CategoriesSerializer,
    GenresSerializer,
    TitlesCreateSerializer,
    TitlesReadSerializer,
)
from .filters import TitlesFilter


class CreateListDestroyViewSet(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class Registration(APIView):
    def post(self, request):
        serializer = SendEmailSerializer(data=request.data)
        if serializer.is_valid() == False:
            return Response('Invalid date', status=status.HTTP_400_BAD_REQUEST)
        email = serializer.data['email']
        username = serializer.data['username']
        if username == 'me':
            return Response(
                'username used', status=status.HTTP_400_BAD_REQUEST
            )
        confirmation_code = random.randint(1111, 9999)
        User.objects.get_or_create(
            email=email,
            username=username,
            confirmation_code=confirmation_code,
            is_active=False,
        )

        send_mail(
            'Welcome to yamdb',
            f'code: {confirmation_code}',
            EMAIL_FROM,
            [email],
            fail_silently=True,
        )
        return Response(status=status.HTTP_200_OK)


# @csrf_exempt
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
            return Response('Error username', status=status.HTTP_404_NOT_FOUND)
        if confirmation_code != user.confirmation_code:
            return Response('Error code', status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken.for_user(user).access_token
        user.is_active = True
        user.save()
        return Response(f'token: {str(token)}', status=status.HTTP_200_OK)


class ReviewsViewSet(viewsets.ModelViewSet):
    """Класс для работы с оценками."""

    serializer_class = ReviewsSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

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
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

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


class CategoriesViewSet(CreateListDestroyViewSet):
    """Вьюсет для категории."""

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class GenresViewSet(CreateListDestroyViewSet):
    """Вьюсет для жанра."""

    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений"""

    queryset = (
        Titles.objects.all()
        .annotate(rating=Avg('reviews__score'))
        .order_by('name')
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = TitlesFilter
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TitlesReadSerializer
        return TitlesCreateSerializer
