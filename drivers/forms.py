from django import forms
from .models import DriverStatus

class DriverCreateForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput,label="Confirm Password")
    phone = forms.CharField(max_length=15)
    employee_id = forms.CharField(max_length=20)
    vehicle_number = forms.CharField(max_length=20)
    license_number = forms.CharField(max_length=50,required=False)

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get(
            "password")

        confirm_password = cleaned_data.get(
            "confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match.")

        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

class DriverStatusForm(forms.ModelForm):

    class Meta:

        model = DriverStatus

        fields = [
            "status",
            "destination",
            "purpose",
            "remarks",
            "expected_return",
        ]

        widgets = {

            "status": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "destination": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "purpose": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),

            "expected_return": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time"
                }
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        status = cleaned_data.get("status")
        destination = cleaned_data.get("destination")
        purpose = cleaned_data.get("purpose")

        if status == "ON_DUTY":

            if not destination:

                raise forms.ValidationError(
                    "Destination is required for On Duty."
                )

            if not purpose:

                raise forms.ValidationError(
                    "Purpose is required for On Duty."
                )

        return cleaned_data
class DriverEditForm(forms.Form):

    full_name = forms.CharField(
        max_length=100
    )

    phone = forms.CharField(
        max_length=15
    )

    employee_id = forms.CharField(
        max_length=20
    )

    vehicle_number = forms.CharField(
        max_length=20,
        required=False
    )

    license_number = forms.CharField(
        max_length=50,
        required=False
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update(
                {
                    "class": "form-control"
                }
            )
class ResetPasswordForm(forms.Form):

    password = forms.CharField(
        widget=forms.PasswordInput,
        label="New Password"
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password"
    )

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get(
            "password"
        )

        confirm_password = cleaned_data.get(
            "confirm_password"
        )

        if password != confirm_password:

            raise forms.ValidationError(
                "Passwords do not match."
            )

        return cleaned_data

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update(
                {
                    "class": "form-control"
                }
            )


