from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from logs.models import ActivityLog
from .models import DriverStatus
from .forms import DriverStatusForm
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth import get_user_model
from .models import DriverProfile, DriverStatus
from .forms import (DriverCreateForm,DriverEditForm,ResetPasswordForm)

@login_required
@never_cache
def update_status(request, status_id):

    driver_status = get_object_or_404(
        DriverStatus,
        id=status_id
    )
    if request.user.role == "DRIVER":

        if driver_status.driver.user != request.user:

            return HttpResponse("You cannot edit another driver's status.")

    if request.method == "POST":

        form = DriverStatusForm(
            request.POST,
            instance=driver_status
        )

        if form.is_valid():

           original_status = DriverStatus.objects.get( id=driver_status.id).status
           updated_status = form.save()
           if original_status != updated_status.status:

                ActivityLog.objects.create(
                driver=updated_status.driver,
            changed_by=request.user,
            old_status=original_status,
            new_status=updated_status.status,
            destination=updated_status.destination,
            purpose=updated_status.purpose,
            remarks=updated_status.remarks,)

        return redirect("dashboard")

    else:

        form = DriverStatusForm(
            instance=driver_status
        )

    return render(
        request,
        "drivers/update_status.html",
        {
            "form": form,
            "driver_status": driver_status,
        },
    )
@login_required
@never_cache
def driver_dashboard(request):

    driver_profile = request.user.driverprofile

    driver_status = DriverStatus.objects.get(
        driver=driver_profile
    )

    return render(
        request,
        "drivers/driver_dashboard.html",
        {
            "driver_status": driver_status,
        }
    )
@login_required
def add_driver(request):

    if request.user.role != "ADMIN":
        return HttpResponse(
            "Only admin can add drivers."
        )

    if request.method == "POST":

        form = DriverCreateForm(
            request.POST
        )

        if form.is_valid():

            User = get_user_model()

            full_name = form.cleaned_data["full_name"]

            first_name = full_name.split()[0]

            last_name = " ".join(
                full_name.split()[1:]
            )

            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
                phone=form.cleaned_data["phone"],
                role="DRIVER",
                first_name=first_name,
                last_name=last_name
            )

            driver = DriverProfile.objects.create(
                user=user,
                employee_id=form.cleaned_data["employee_id"],
                vehicle_number=form.cleaned_data["vehicle_number"],
                license_number=form.cleaned_data["license_number"]
            )

            DriverStatus.objects.create(
                driver=driver,
                status="AVAILABLE"
            )

            return redirect(
                "dashboard"
            )

    else:

        form = DriverCreateForm()

    return render(
        request,
        "drivers/add_driver.html",
        {
            "form": form
        }
    )

@login_required
def manage_drivers(request):

    if request.user.role != "ADMIN":
        return HttpResponse(
            "Only admin can access this page."
        )

    drivers = DriverProfile.objects.select_related(
        "user"
    )

    return render(
        request,
        "drivers/manage_drivers.html",
        {
            "drivers": drivers
        }
    )
@login_required
def edit_driver(request, driver_id):

    if request.user.role != "ADMIN":

        return HttpResponse(
            "Only admin can edit drivers."
        )

    driver = get_object_or_404(
        DriverProfile,
        id=driver_id
    )

    if request.method == "POST":

        form = DriverEditForm(
            request.POST
        )

        if form.is_valid():

            full_name = form.cleaned_data[
                "full_name"
            ]

            driver.user.first_name = (
                full_name.split()[0]
            )

            driver.user.last_name = " ".join(
                full_name.split()[1:]
            )

            driver.user.phone = form.cleaned_data[
                "phone"
            ]

            driver.user.save()

            driver.employee_id = form.cleaned_data[
                "employee_id"
            ]

            driver.vehicle_number = form.cleaned_data[
                "vehicle_number"
            ]

            driver.license_number = form.cleaned_data[
                "license_number"
            ]

            driver.save()

            return redirect(
                "manage_drivers"
            )

    else:

        form = DriverEditForm(
            initial={
                "full_name":
                driver.user.get_full_name(),

                "phone":
                driver.user.phone,

                "employee_id":
                driver.employee_id,

                "vehicle_number":
                driver.vehicle_number,

                "license_number":
                driver.license_number,
            }
        )

    return render(
        request,
        "drivers/edit_driver.html",
        {
            "form": form,
            "driver": driver
        }
    )
@login_required
def delete_driver(request, driver_id):

    if request.user.role != "ADMIN":

        return HttpResponse(
            "Only admin can delete drivers."
        )

    driver = get_object_or_404(
        DriverProfile,
        id=driver_id
    )

    if request.method == "POST":

        if driver.user.role == "ADMIN":

            return HttpResponse(
               "Admin account cannot be deleted."
        )

        driver.user.delete()

        return redirect(
           "manage_drivers"
    )

    return render(
        request,
        "drivers/delete_driver.html",
        {
            "driver": driver
        }
    )

@login_required
def reset_password(request, driver_id):

    if request.user.role != "ADMIN":

        return HttpResponse(
            "Only admin can reset passwords."
        )

    driver = get_object_or_404(
        DriverProfile,
        id=driver_id
    )

    if request.method == "POST":

        form = ResetPasswordForm(
            request.POST
        )

        if form.is_valid():

            driver.user.set_password(
                form.cleaned_data["password"]
            )

            driver.user.save()

            return redirect(
                "manage_drivers"
            )

    else:

        form = ResetPasswordForm()

    return render(
        request,
        "drivers/reset_password.html",
        {
            "form": form,
            "driver": driver
        }
    )

@login_required
def activity_logs(request):

    if request.user.role != "ADMIN":

        return HttpResponse(
            "Only admin can access logs."
        )

    logs = ActivityLog.objects.select_related(
        "driver",
        "changed_by"
    ).order_by(
        "-timestamp"
    )

    return render(
        request,
        "drivers/activity_logs.html",
        {
            "logs": logs
        }
    )