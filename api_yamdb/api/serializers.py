from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from reviews.models import Comments, Reviews, Titles, User, Categories, Genres


class SendEmailSerializer(serializers.ModelSerializer):
    """Сериализатор для функции регистрации"""
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'username')


class SendTokenSerializer(serializers.ModelSerializer):
    """Сериализатор для функции предоставления токена."""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор данных пользователя"""
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'bio',
            'email',
            'role',
        )


class ReviewsSerializer(serializers.ModelSerializer):
    """Класс для преобразования данных отзыва."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        many=False,
    )

    def validate(self, attr):
        request = self.context['request']
        if request.method != 'POST':
            return attr
        author = request.user
        title_id = request.kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        if Reviews.objects.filter(title=title, author=author).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на данное произведение'
            )
        return attr

    class Meta:
        model = Reviews
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentsSerializer(serializers.ModelSerializer):
    """Класс для преобразования данных комментария."""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date')


class CategoriesSerializer(serializers.ModelSerializer):
    """Класс сериализатор категории."""

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    """Класс сериализатор жанра."""

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class TitlesReadSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(many=True, read_only=True)

    class Meta:
        fields = '__all__'
        model = Titles


class TitlesCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(), slug_field='slug', many=True
    )

    class Meta:
        fields = '__all__'
        model = Titles
