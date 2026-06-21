from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User
from drivers.models import DriverProfile, DriverStatus


@receiver(post_save, sender=User)
def create_driver_profile(sender, instance, created, **kwargs):

    if created and instance.role == "DRIVER":

        profile = DriverProfile.objects.create(
            user=instance,
            employee_id=f"DRV{instance.id:04d}"
        )

        DriverStatus.objects.create(
            driver=profile
        )