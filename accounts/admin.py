from django.contrib import admin
from .models import *

# Register your models here.


@admin.decorators.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
