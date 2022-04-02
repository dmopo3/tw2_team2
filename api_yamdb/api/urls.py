from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentsViewSet, Registration, ReviewsViewSet, SendToren

router = DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)' r'/comments',
    CommentsViewSet,
    basename='comments',
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', Registration.as_view()),
    path('v1/auth/token/', SendToren),
]
