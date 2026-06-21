from django.conf import settings
from django.db import models
from drivers.models import DriverProfile


class ActivityLog(models.Model):

    driver = models.ForeignKey(
        DriverProfile,
        on_delete=models.CASCADE
    )

    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    old_status = models.CharField(
        max_length=20
    )

    new_status = models.CharField(
        max_length=20
    )

    destination = models.CharField(
        max_length=255,
        blank=True
    )

    purpose = models.CharField(
        max_length=255,
        blank=True
    )

    remarks = models.TextField(
        blank=True
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self):
        return f"{self.driver}"