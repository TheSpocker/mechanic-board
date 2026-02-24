from django.contrib import admin
from .models import (
    WorkOrder,
    RentalCar,
    RentalAgreement,
    RentalIssue,
    CarForSale,
    CarForSaleIssue,
)


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ("status", "vehicle", "plate", "customer", "promised_date", "updated_at")
    list_filter = ("status",)
    search_fields = ("vehicle", "plate", "customer", "complaint")


@admin.register(RentalCar)
class RentalCarAdmin(admin.ModelAdmin):
    list_display = ("status", "vehicle", "plate", "updated_at")
    list_filter = ("status",)
    search_fields = ("vehicle", "plate")


@admin.register(RentalAgreement)
class RentalAgreementAdmin(admin.ModelAdmin):
    list_display = ("status", "rental_car", "renter_name", "start_date", "due_date", "return_date")
    list_filter = ("status",)
    search_fields = ("renter_name", "renter_phone", "rental_car__plate")


@admin.register(RentalIssue)
class RentalIssueAdmin(admin.ModelAdmin):
    list_display = ("status", "severity", "rental_car", "title", "reported_date", "resolved_date")
    list_filter = ("status", "severity")
    search_fields = ("rental_car__plate", "title", "description")


@admin.register(CarForSale)
class CarForSaleAdmin(admin.ModelAdmin):
    list_display = ("status", "year", "make", "model", "trim", "mileage", "price", "plate", "updated_at")
    list_filter = ("status", "make")
    search_fields = ("vin", "plate", "make", "model", "trim", "known_issues", "notes")


@admin.register(CarForSaleIssue)
class CarForSaleIssueAdmin(admin.ModelAdmin):
    list_display = ("status", "severity", "car", "title", "created_at")
    list_filter = ("status", "severity")
    search_fields = ("title", "description", "car__vin", "car__plate", "car__make", "car__model")
