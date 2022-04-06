from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CommentsViewSet,
    CategoriesViewSet,
    GenresViewSet,
    TitlesViewSet,
    Registration,
    ReviewsViewSet,
    SendToren
)

router = DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)' r'/comments',
    CommentsViewSet,
    basename='comments',
)
router.register('categories', CategoriesViewSet)
router.register('genres', GenresViewSet)
router.register('titles', TitlesViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', Registration.as_view()),
    path('v1/auth/token/', SendToren.as_view()),
]
