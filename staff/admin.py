from django.contrib import admin
from .models import ClinicStaffAssignment, Staff, SupportStaff ,TechnicalStaff, DutyRoster
 
models = [ClinicStaffAssignment, Staff, SupportStaff ,TechnicalStaff, DutyRoster]
# Register your models here.
admin.site.register(models)