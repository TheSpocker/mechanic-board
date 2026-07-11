import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import WorkOrder


def board_view(request):
    workorders = WorkOrder.objects.exclude(
        status__in=["DONE", "CANCELLED"]
    ).order_by("status", "-updated_at")

    return render(request, "board/board.html", {
        "workorders": workorders
    })


def _serialize_workorder(workorder):
    return {
        "id": workorder.id,
        "plate": workorder.plate,
        "vehicle": workorder.vehicle,
        "customer": workorder.customer,
        "complaint": workorder.complaint,
        "status": workorder.status,
        "promised_date": workorder.promised_date.isoformat() if workorder.promised_date else None,
        "created_at": workorder.created_at.isoformat(),
        "updated_at": workorder.updated_at.isoformat(),
    }


def workorder_list(request):
    if request.method == "GET":
        workorders = WorkOrder.objects.all().order_by("-updated_at", "-id")
        return JsonResponse({
            "count": workorders.count(),
            "results": [_serialize_workorder(order) for order in workorders],
        })

    return JsonResponse({"detail": "Method not allowed"}, status=405)


def workorder_detail(request, pk):
    workorder = get_object_or_404(WorkOrder, pk=pk)

    if request.method == "GET":
        return JsonResponse(_serialize_workorder(workorder))

    if request.method == "PATCH":
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return JsonResponse({"detail": "Invalid JSON"}, status=400)

        allowed_fields = {"status", "plate", "vehicle", "customer", "complaint", "promised_date"}
        for field, value in payload.items():
            if field not in allowed_fields:
                continue
            setattr(workorder, field, value)

        workorder.save(update_fields=payload.keys())
        return JsonResponse(_serialize_workorder(workorder))

    return JsonResponse({"detail": "Method not allowed"}, status=405)
