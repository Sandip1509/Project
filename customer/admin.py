from django.contrib import admin

# Register your models here.
from .models import CustomerProfile

admin.site.register(CustomerProfile)