from django.contrib import admin
from .models import Title, Review, Category, Comment, Genre, User
from django.contrib.auth.admin import UserAdmin

admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Genre)


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Additional Info',
            {
                'fields': (
                    'role',
                    'bio'
                )
            }
        )
    )


admin.site.register(User, CustomUserAdmin)