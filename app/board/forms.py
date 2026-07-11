from django import forms
from django.forms import inlineformset_factory

from .models import RentalAgreement, WorkOrder, WorkOrderLineItem


class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = [
            "customer",
            "customer_phone",
            "vehicle",
            "plate",
            "vin",
            "mileage",
            "check_in",
            "check_out",
            "complaint",
            "intervention_1",
            "intervention_2",
            "intervention_3",
            "intervention_4",
            "intervention_5",
            "intervention_6",
            "intervention_7",
            "intervention_8",
            "status",
            "promised_date",
            "notes",
        ]
        widgets = {
            "check_in": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "check_out": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "promised_date": forms.DateInput(attrs={"type": "date"}),
            "complaint": forms.Textarea(attrs={"rows": 3}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }


WorkOrderLineItemFormSet = inlineformset_factory(
    WorkOrder,
    WorkOrderLineItem,
    fields=["quantity", "description", "unit_price", "position"],
    extra=8,
    can_delete=True,
)


class RentalAgreementForm(forms.ModelForm):
    class Meta:
        model = RentalAgreement
        fields = [
            "rental_car",
            "renter_name",
            "renter_phone",
            "language",
            "fuel_type",
            "start_date",
            "start_time",
            "due_date",
            "return_date",
            "return_time",
            "status",
            "notes",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "return_date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "return_time": forms.TimeInput(attrs={"type": "time"}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }
