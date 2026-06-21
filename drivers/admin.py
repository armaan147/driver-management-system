from django.contrib import admin
from .models import DriverProfile, DriverStatus


@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "employee_id",
        "vehicle_number",
        "license_number",
    )


@admin.register(DriverStatus)
class DriverStatusAdmin(admin.ModelAdmin):

    list_display = (
        "driver",
        "status",
        "destination",
        "updated_at",
    )