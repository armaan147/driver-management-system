from django.contrib import admin
from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):

    list_display = (
        "driver",
        "changed_by",
        "old_status",
        "new_status",
        "timestamp",
    )

    ordering = ("-timestamp",)