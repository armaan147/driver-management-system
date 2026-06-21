from django.conf import settings
from django.db import models


class DriverProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    employee_id = models.CharField(
        max_length=20,
        unique=True
    )
    vehicle_number = models.CharField(
    max_length=20,
    blank=True)

    license_number = models.CharField(
    max_length=50,
    blank=True )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.get_full_name()


class DriverStatus(models.Model):

    STATUS_CHOICES = [
        ("AVAILABLE", "Available"),
        ("ON_DUTY", "On Duty"),
        ("LEAVE", "Leave"),
        ("OFF_DUTY", "Off Duty"),
    ]

    driver = models.OneToOneField(
        DriverProfile,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="AVAILABLE"
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
    expected_return = models.TimeField(
    null=True,
    blank=True
)
    updated_at = models.DateTimeField(auto_now=True )

    def __str__(self):
        return f"{self.driver.user.username} - {self.status}"
    