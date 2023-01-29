from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from .utils import max_value_current_year, current_year


class User(AbstractUser):
    ROLES = (
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    )
    email = models.EmailField(max_length=255, unique=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    role = models.CharField(max_length=50, choices=ROLES, default='user')
    confirmation_code = models.CharField(max_length=200, null=True, blank=True)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.PositiveIntegerField(
        default=current_year(), validators=[MinValueValidator(1700), max_value_current_year]
    )
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(default=0)
    description = models.TextField(max_length=500, blank=True, null=True)
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.name


class Review(models.Model):
    CHOICES = [(i, i) for i in range(11)]

    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    score = models.PositiveSmallIntegerField(default=10, choices=CHOICES)
    pub_date = models.DateTimeField("Review published", auto_now_add=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True)

    def __str__(self):
        return self.text