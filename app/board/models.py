from django.db import models


class WorkOrder(models.Model):

    STATUS_CHOICES = [
        ("SCHEDULED", "Scheduled"),
        ("CHECKED_IN", "Checked In"),
        ("DIAG", "Diagnosing"),
        ("WAIT_CUST", "Waiting on Customer"),
        ("WAIT_PARTS", "Waiting on Parts"),
        ("IN_PROGRESS", "In Progress"),
        ("READY", "Ready for Pickup"),
        ("DONE", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]

    plate = models.CharField(max_length=20, blank=True)
    vehicle = models.CharField(max_length=100)
    customer = models.CharField(max_length=100, blank=True)
    complaint = models.CharField(max_length=255, blank=True)

    customer_phone = models.CharField(max_length=30, blank=True)
    vin = models.CharField(max_length=17, blank=True)
    mileage = models.PositiveIntegerField(null=True, blank=True)

    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)

    intervention_1 = models.CharField(max_length=255, blank=True)
    intervention_2 = models.CharField(max_length=255, blank=True)
    intervention_3 = models.CharField(max_length=255, blank=True)
    intervention_4 = models.CharField(max_length=255, blank=True)
    intervention_5 = models.CharField(max_length=255, blank=True)
    intervention_6 = models.CharField(max_length=255, blank=True)
    intervention_7 = models.CharField(max_length=255, blank=True)
    intervention_8 = models.CharField(max_length=255, blank=True)

    notes = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="CHECKED_IN",
    )

    promised_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def subtotal(self):
        return sum(
            (item.line_total for item in self.line_items.all()),
            start=0,
        )

    @property
    def total(self):
        return self.subtotal

    def __str__(self):
        return f"{self.vehicle} ({self.plate}) - {self.status}"


class WorkOrderLineItem(models.Model):
    work_order = models.ForeignKey(
        WorkOrder,
        on_delete=models.CASCADE,
        related_name="line_items",
    )

    quantity = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=1,
    )

    description = models.CharField(
        max_length=255,
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    position = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        ordering = ["position", "id"]

    @property
    def line_total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.quantity} x {self.description}"


class RentalCar(models.Model):

    STATUS_CHOICES = [
        ("AVAILABLE", "Available"),
        ("RENTED", "Rented"),
        ("MAINT", "Needs Maintenance"),
        ("OUT", "Out of Service"),
    ]

    vehicle = models.CharField(max_length=100)
    plate = models.CharField(max_length=20, unique=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="AVAILABLE",
    )

    notes = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vehicle} ({self.plate})"


class RentalAgreement(models.Model):

    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("RETURNED", "Returned"),
        ("LATE", "Late"),
    ]

    LANGUAGE_CHOICES = [
        ("EN", "English"),
        ("IT", "Italian"),
    ]

    rental_car = models.ForeignKey(
        RentalCar,
        on_delete=models.PROTECT,
        related_name="rentals",
    )

    renter_name = models.CharField(max_length=100)
    renter_phone = models.CharField(max_length=30, blank=True)

    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default="IT",
    )

    fuel_type = models.CharField(max_length=50, blank=True)

    start_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    start_time = models.TimeField(null=True, blank=True)
    return_time = models.TimeField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="OPEN",
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.rental_car.plate} - "
            f"{self.renter_name} ({self.status})"
        )


class RentalIssue(models.Model):

    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("IN_PROGRESS", "In Progress"),
        ("RESOLVED", "Resolved"),
    ]

    SEVERITY_CHOICES = [
        ("LOW", "Low"),
        ("MED", "Medium"),
        ("HIGH", "High"),
    ]

    rental_car = models.ForeignKey(
        RentalCar,
        on_delete=models.CASCADE,
        related_name="issues",
    )

    rental_agreement = models.ForeignKey(
        RentalAgreement,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="issues",
    )

    title = models.CharField(max_length=120)
    description = models.CharField(max_length=255, blank=True)

    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_CHOICES,
        default="MED",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="OPEN",
    )

    reported_date = models.DateField(null=True, blank=True)
    resolved_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return (
            f"{self.rental_car.plate} - "
            f"{self.title} ({self.status})"
        )


class CarForSale(models.Model):

    STATUS_CHOICES = [
        ("AVAILABLE", "Available"),
        ("PENDING", "Pending"),
        ("SOLD", "Sold"),
        ("HOLD", "Hold"),
    ]

    year = models.PositiveIntegerField(null=True, blank=True)
    make = models.CharField(max_length=40, blank=True)
    model = models.CharField(max_length=60, blank=True)
    trim = models.CharField(max_length=60, blank=True)

    mileage = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    plate = models.CharField(max_length=20, blank=True)
    vin = models.CharField(max_length=17, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="AVAILABLE",
    )

    known_issues = models.CharField(max_length=255, blank=True)
    notes = models.CharField(max_length=255, blank=True)

    listed_date = models.DateField(null=True, blank=True)
    photos_url = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        title = " ".join(
            value
            for value in [
                str(self.year or ""),
                self.make,
                self.model,
                self.trim,
            ]
            if value
        ).strip()

        return (
            f"{title or 'Car'} - "
            f"€{self.price} - "
            f"{self.mileage} mi"
        )


class CarForSaleIssue(models.Model):

    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("RESOLVED", "Resolved"),
    ]

    SEVERITY_CHOICES = [
        ("LOW", "Low"),
        ("MED", "Medium"),
        ("HIGH", "High"),
    ]

    car = models.ForeignKey(
        CarForSale,
        on_delete=models.CASCADE,
        related_name="issues",
    )

    title = models.CharField(max_length=120)
    description = models.CharField(max_length=255, blank=True)

    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_CHOICES,
        default="MED",
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="OPEN",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car_id} - {self.title} ({self.status})"