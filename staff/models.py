# staff/models.py
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings  # CustomUser
from clinics.models import Clinic


class TechnicalStaff(models.Model):
    """Predefined technical roles (e.g., Nurse, Lab Technician)."""
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class SupportStaff(models.Model):
    """Predefined support roles (e.g., Receptionist, Cleaner)."""
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Staff(models.Model):
    EMPLOYMENT_TYPES = [
        ('technical', 'Technical Staff'),
        ('support', 'Support Staff'),
    ]
    ACCOUNT_STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    DUTY_STATUS = [
        ('on_duty', 'On Duty'),
        ('on_leave', 'On Leave'),
        ('off_duty', 'Off Duty'),
    ]

    # Link to your custom user model
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='staff_profile')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_staff')

    # Clinic assignment through a join model
    clinics = models.ManyToManyField(Clinic, through='ClinicStaffAssignment', related_name='assigned_staff')

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17)
    date_of_birth = models.DateField()
    national_id = models.CharField(max_length=50, unique=True)
    profile_picture = models.ImageField(upload_to='staff_pics/', blank=True, null=True)

    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPES)

    # Role references
    technical_role = models.ForeignKey(TechnicalStaff, on_delete=models.SET_NULL, null=True, blank=True)
    support_role = models.ForeignKey(SupportStaff, on_delete=models.SET_NULL, null=True, blank=True)

    registration_number = models.CharField(max_length=100, blank=True, null=True)
    license_expiry_date = models.DateField(blank=True, null=True)

    next_of_kin = models.CharField(max_length=200)
    nok_relationship = models.CharField(max_length=50)
    nok_phone = models.CharField(validators=[phone_regex], max_length=17)

    gross_salary = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    monthly_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)])

    account_status = models.CharField(max_length=10, choices=ACCOUNT_STATUS, default='active')
    duty_status = models.CharField(max_length=10, choices=DUTY_STATUS, default='on_duty')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # enforce role consistency
        if self.employment_type == 'technical' and not self.technical_role:
            raise ValidationError("Technical staff must have a technical role.")
        if self.employment_type == 'support' and not self.support_role:
            raise ValidationError("Support staff must have a support role.")

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_employment_type_display()})"


class ClinicStaffAssignment(models.Model):
    """Tracks which clinic owner assigned which staff to which clinic."""
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('clinic', 'staff')
        db_table = 'clinic_staff_assignment'  # 👈 avoids clash

    def __str__(self):
        return f"{self.staff} → {self.clinic} (assigned by {self.assigned_by})"


class DutyRoster(models.Model):
    """Duty roster for assigning staff to specific days/shifts."""
    SHIFT_CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('night', 'Night'),
    ]

    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='duty_rosters')
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='duty_rosters')
    date = models.DateField()
    shift = models.CharField(max_length=20, choices=SHIFT_CHOICES, blank=True, null=True)
    notes = models.TextField(blank=True)

    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_duties'
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('clinic', 'staff', 'date', 'shift')
        ordering = ['date', 'shift']

    def __str__(self):
        return f"{self.staff} → {self.clinic} on {self.date} ({self.shift or 'unspecified'})"
