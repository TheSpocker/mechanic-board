import json

from django.test import TestCase
from django.urls import reverse

from .models import WorkOrder


class WorkOrderApiTests(TestCase):
    def test_list_workorders_endpoint_returns_existing_records(self):
        WorkOrder.objects.create(vehicle="Ford Focus", status="CHECKED_IN")

        response = self.client.get(reverse("workorder-list"))

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["results"][0]["vehicle"], "Ford Focus")

    def test_update_workorder_endpoint_changes_status(self):
        workorder = WorkOrder.objects.create(vehicle="Toyota Corolla", status="CHECKED_IN")

        response = self.client.patch(
            reverse("workorder-detail", args=[workorder.pk]),
            data=json.dumps({"status": "READY"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        workorder.refresh_from_db()
        self.assertEqual(workorder.status, "READY")
