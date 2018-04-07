from django.contrib import admin

from organiser.models import Profile


@admin.register(Profile)
class AuthorAdmin(admin.ModelAdmin):
    pass