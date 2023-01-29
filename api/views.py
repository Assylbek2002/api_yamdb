from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
import api_yamdb.settings as settings
from .permissions import *
from .serializers import *
from .utils import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import User
from rest_framework.permissions import *


@api_view(['POST'])
def api_get_token(request):
    email = request.data.get('email')
    code = request.data.get('confirmation_code')
    user = get_object_or_404(User, email=email)
    if code == user.confirmation_code:
        user.confirmation_code = ''
        token = get_tokens_for_user(user)
        return Response(token)
    return Response("Invalid credentials", status=404)


@api_view(['POST'])
@permission_classes([AllowAny])
def api_send_confirmation_code(request):
    confirmation_code = str(code_generator())
    receiver = request.data.get('email')
    subject = 'Confirm your code'
    send_mail(
        subject=subject,
        message=f"Your code is {confirmation_code}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[receiver]
    )
    user = get_object_or_404(User, email=receiver)
    user.confirmation_code = confirmation_code
    user.save()
    return Response({"email": f"{receiver}"})


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def api_about_me(request):
    if request.method == 'GET':
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == "PATCH":
        user = request.user
        serializer = UserSerializer(user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [AdminOrAnyPermission, ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'genre', 'name', 'year']


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AdminOrAnyPermission, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminOrAnyPermission, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AdminOrAnyOrAuthPermission, ]

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=int(self.kwargs.get('title_id')))
        temp = int(self.request.data['score']) + title.rating
        review_count = title.reviews.count() + 1
        title.rating = int(temp/review_count)
        title.save()
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        reviews = Review.objects.filter(title=title)
        return reviews


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AdminOrAnyOrAuthPermission, ]


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdministrator, ]
    lookup_field = 'username'
