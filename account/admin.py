from django.contrib import admin
from .models import CustomUser, UserAddress, CompanyAddress, Company

models = [CustomUser, UserAddress, CompanyAddress, Company]
for model in models:
    admin.site.register(model)
