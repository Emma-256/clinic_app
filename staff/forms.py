from django import forms
from django.contrib.auth import get_user_model
from .models import Staff, TechnicalStaff, SupportStaff
import re

User = get_user_model()


class StaffRegistrationForm(forms.ModelForm):
    # ── User account fields ──────────────────────────────
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username for this staff member',
        })
    )
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name',
        })
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address',
        })
    )

    phone = forms.CharField(
        max_length=13,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': '+256XXXXXXXXX'})
    )
    
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Set a password for this staff member',
        })
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password',
        })
    )

    class Meta:
        model = Staff
        fields = [
            # User fields handled above
            'username', 'first_name', 'last_name','phone', 'email', 'password1', 'password2',
            # Staff fields
            'date_of_birth', 'national_id', 'profile_picture',
            'employment_type',
            'technical_role', 'support_role',
            'registration_number', 'license_expiry_date',
            'next_of_kin', 'nok_relationship', 'nok_phone',
            'gross_salary', 'monthly_allowance',
            'account_status', 'duty_status',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'national_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'National ID number',
            }),
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'employment_type': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_employment_type',
            }),
            'technical_role': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_technical_role',
            }),
            'support_role': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_support_role',
            }),
            'registration_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Professional registration number (if applicable)',
            }),
            'license_expiry_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'next_of_kin': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Next of kin full name',
            }),
            'nok_relationship': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Relationship (e.g. Spouse, Parent)',
            }),
            'nok_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+256XXXXXXXXX',
            }),
            'gross_salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 1500000',
            }),
            'monthly_allowance': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 200000',
            }),
            'account_status': forms.Select(attrs={
                'class': 'form-select',
            }),
            'duty_status': forms.Select(attrs={
                'class': 'form-select',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.label = ''
            field.help_text = None

        # Always allow all roles — visibility is controlled by JS, not queryset
        self.fields['technical_role'].queryset = TechnicalStaff.objects.all()
        self.fields['technical_role'].required = False
        self.fields['technical_role'].empty_label = '— Select Technical Role —'

        self.fields['support_role'].queryset = SupportStaff.objects.all()
        self.fields['support_role'].required = False
        self.fields['support_role'].empty_label = '— Select Support Role —'

    # ── Validation ───────────────────────────────────────

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\+256\d{9}$', phone):
            raise forms.ValidationError("Phone must be in format +256XXXXXXXXX.")
        return phone

    def clean_nok_phone(self):
        nok_phone = self.cleaned_data.get('nok_phone')
        if not re.match(r'^\+256\d{9}$', nok_phone):
            raise forms.ValidationError("NOK phone must be in format +256XXXXXXXXX.")
        return nok_phone

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return p2

    def clean(self):
        cleaned_data = super().clean()
        employment_type = cleaned_data.get('employment_type')
        technical_role  = cleaned_data.get('technical_role')
        support_role    = cleaned_data.get('support_role')

        if employment_type == 'technical':
            if not technical_role:
                self.add_error('technical_role', 'Please select a technical role.')
            cleaned_data['support_role'] = None

        elif employment_type == 'support':
            if not support_role:
                self.add_error('support_role', 'Please select a support role.')
            cleaned_data['technical_role'] = None

        return cleaned_data

    # ── Save ─────────────────────────────────────────────

    def save(self, commit=True, created_by=None):
        # 1. Create the User account
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            phone=self.cleaned_data['phone'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            is_active=True,   # active from the start — owner gave them the password
        )

        # 2. Mark as staff (mirrors how owners are marked via UserProfile)
        from clinic_owners.models import UserProfile
        UserProfile.objects.create(
            user=user,
            user_type='staff',  # distinguishes them from owners
        )

        # 3. Create the Staff record
        staff = super().save(commit=False)
        staff.user = user
        staff.created_by = created_by

        if commit:
            staff.save()

        return staff