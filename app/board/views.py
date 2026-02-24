from django.shortcuts import render
from .models import WorkOrder


def board_view(request):
    workorders = WorkOrder.objects.exclude(
        status__in=["DONE", "CANCELLED"]
    ).order_by("status", "-updated_at")

    return render(request, "board/board.html", {
        "workorders": workorders
    })
