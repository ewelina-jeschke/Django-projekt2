# Django
from django.contrib import admin

# Project
from users.models import ExtendedUser


@admin.register(ExtendedUser)
class ExtendedUserAdmin(admin.ModelAdmin):
    pass
