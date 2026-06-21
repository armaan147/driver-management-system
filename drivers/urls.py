from django.urls import path
from .views import update_status, driver_dashboard
from . import views
from .views import manage_drivers
from .views import edit_driver
from .views import delete_driver
from .views import reset_password
from .views import activity_logs

urlpatterns = [

    path(
        "manage/",
        manage_drivers,
        name="manage_drivers"
    ),

    path(
        "add-driver/",
        views.add_driver,
        name="add_driver"
    ),

    path(
        "status/<int:status_id>/",
        update_status,
        name="update_status",
    ),

    path(
        "dashboard/",
        driver_dashboard,
        name="driver_dashboard",
    ),
    path(
    "edit/<int:driver_id>/",
    edit_driver,
    name="edit_driver"
),
path(
    "delete/<int:driver_id>/",
    delete_driver,
    name="delete_driver"
),
path(
    "reset-password/<int:driver_id>/",
    reset_password,
    name="reset_password"
),
path(
    "logs/",
    activity_logs,
    name="activity_logs"
),
]