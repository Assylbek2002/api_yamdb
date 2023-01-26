from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('auth/token/', api_get_token),
    path('auth/email/', api_send_confirmation_code),
]

router = DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('titles/(?P<title_id>[0-9]+)/reviews', ReviewViewSet, basename='reviews')
router.register('titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+/comments)', CommentViewSet, basename='comments')
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register('users', UserViewSet, basename='users')
urlpatterns += router.urls



