from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.utils import timezone

from drivers.models import DriverStatus
from logs.models import ActivityLog

@login_required
@never_cache
def dashboard(request):
    # AUTO RETURN FEATURE

    current_time = timezone.localtime().time()

    expired_drivers = DriverStatus.objects.filter(
        status="ON_DUTY",
        expected_return__isnull=False
    )

    for driver in expired_drivers:

        if driver.expected_return <= current_time:

            old_status = driver.status

            driver.status = "AVAILABLE"
            driver.destination = ""
            driver.purpose = ""
            driver.remarks = ""
            driver.expected_return = None

            driver.save()

            ActivityLog.objects.create(
                driver=driver.driver,
                changed_by=None,
                old_status=old_status,
                new_status="AVAILABLE",
                destination="",
                purpose="",
                remarks="Auto return completed"
            )

    # DASHBOARD DATA

    statuses = DriverStatus.objects.select_related(
        "driver",
        "driver__user"
    )

    available_drivers = statuses.filter(
        status="AVAILABLE"
    )

    recent_logs = ActivityLog.objects.select_related(
        "driver",
        "changed_by"
    ).order_by(
        "-timestamp"
    )[:5]

    context = {

        "available_count":
            statuses.filter(
                status="AVAILABLE"
            ).count(),

        "on_duty_count":
            statuses.filter(
                status="ON_DUTY"
            ).count(),

        "leave_count":
            statuses.filter(
                status="LEAVE"
            ).count(),

        "off_duty_count":
            statuses.filter(
                status="OFF_DUTY"
            ).count(),

        "statuses": statuses,

        "available_drivers":
            available_drivers,

        "recent_logs":
            recent_logs,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )
