from django.contrib import admin
from .models import Day, Department, Clinic, District, County, Parish, Village, Subcounty

models = [Day, Department, Clinic, District, County, Parish, Village, Subcounty ]
# Register your models here.
admin.site.register(models)



