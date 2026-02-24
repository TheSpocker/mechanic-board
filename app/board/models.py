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

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="CHECKED_IN",
    )

    promised_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vehicle} ({self.plate}) - {self.status}"


class RentalCar(models.Model):

    STATUS_CHOICES = [
        ("AVAILABLE", "Available"),
        ("RENTED", "Rented"),
        ("MAINT", "Needs Maintenance"),
        ("OUT", "Out of Service"),
    ]

    vehicle = models.CharField(max_length=100)     # e.g. "2016 Fiat Panda"
    plate = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="AVAILABLE")

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

    rental_car = models.ForeignKey(RentalCar, on_delete=models.PROTECT, related_name="rentals")

    renter_name = models.CharField(max_length=100)
    renter_phone = models.CharField(max_length=30, blank=True)

    start_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OPEN")

    notes = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.rental_car.plate} - {self.renter_name} ({self.status})"


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

    rental_car = models.ForeignKey(RentalCar, on_delete=models.CASCADE, related_name="issues")
    rental_agreement = models.ForeignKey(RentalAgreement, null=True, blank=True, on_delete=models.SET_NULL, related_name="issues")

    title = models.CharField(max_length=120)
    description = models.CharField(max_length=255, blank=True)

    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default="MED")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OPEN")

    reported_date = models.DateField(null=True, blank=True)
    resolved_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.rental_car.plate} - {self.title} ({self.status})"


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

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="AVAILABLE")

    known_issues = models.CharField(max_length=255, blank=True)
    notes = models.CharField(max_length=255, blank=True)

    listed_date = models.DateField(null=True, blank=True)
    photos_url = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        title = " ".join(x for x in [str(self.year or ""), self.make, self.model, self.trim] if x).strip()
        return f"{title or 'Car'} - €{self.price} - {self.mileage} mi"


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

    car = models.ForeignKey(CarForSale, on_delete=models.CASCADE, related_name="issues")

    title = models.CharField(max_length=120)
    description = models.CharField(max_length=255, blank=True)

    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default="MED")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="OPEN")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car_id} - {self.title} ({self.status})"
