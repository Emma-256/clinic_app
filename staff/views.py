from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import StaffRegistrationForm
from .models import TechnicalStaff, SupportStaff, ClinicStaffAssignment
from clinics.models import Clinic


@login_required
def register_staff(request):
    # Only clinics owned by this user
    owner_clinics = Clinic.objects.filter(owner=request.user)

    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            staff = form.save(created_by=request.user)

            # Assign to selected clinic
            clinic_id = request.POST.get('clinic')
            if clinic_id:
                clinic = get_object_or_404(Clinic, id=clinic_id, owner=request.user)
                ClinicStaffAssignment.objects.create(
                    clinic=clinic,
                    staff=staff,
                    assigned_by=request.user,
                )

            messages.success(request, f"Staff member {staff.user.get_full_name()} registered successfully.")
            return redirect('staff:staff_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StaffRegistrationForm()

    return render(request, 'staff/staff_form.html', {
        'form': form,
        'owner_clinics': owner_clinics,
    })


@login_required
def get_roles(request):
    """AJAX: return roles based on employment type."""
    employment_type = request.GET.get('employment_type')
    roles = []
    if employment_type == 'technical':
        roles = list(TechnicalStaff.objects.values('id', 'name'))
    elif employment_type == 'support':
        roles = list(SupportStaff.objects.values('id', 'name'))
    return JsonResponse({'roles': roles})


@login_required
def toggle_staff_status(request, staff_id):
    """Owner can activate or deactivate a staff member."""
    from .models import Staff
    staff = get_object_or_404(Staff, id=staff_id, created_by=request.user)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')  # 'active' or 'inactive'
        if new_status in ['active', 'inactive']:
            staff.account_status = new_status
            staff.user.is_active = (new_status == 'active')
            staff.user.save()
            staff.save()
            messages.success(request, f"{staff.user.get_full_name()} has been {'activated' if new_status == 'active' else 'deactivated'}.")
    
    return redirect('staff:staff_list')