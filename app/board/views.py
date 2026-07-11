from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import (
    RentalAgreementForm,
    WorkOrderForm,
    WorkOrderLineItemFormSet,
)
from .models import RentalAgreement, WorkOrder


def board_view(request):
    workorders = WorkOrder.objects.exclude(
        status__in=["DONE", "CANCELLED"]
    ).order_by("promised_date", "created_at")

    rentals = RentalAgreement.objects.select_related(
        "rental_car"
    ).order_by("-created_at")[:10]

    return render(
        request,
        "board/board.html",
        {
            "workorders": workorders,
            "rentals": rentals,
        },
    )


@require_http_methods(["GET"])
def workorder_list(request):
    workorders = WorkOrder.objects.all().order_by("-created_at")

    data = [
        {
            "id": workorder.id,
            "plate": workorder.plate,
            "vehicle": workorder.vehicle,
            "customer": workorder.customer,
            "complaint": workorder.complaint,
            "status": workorder.status,
            "promised_date": (
                workorder.promised_date.isoformat()
                if workorder.promised_date
                else None
            ),
            "created_at": workorder.created_at.isoformat(),
            "updated_at": workorder.updated_at.isoformat(),
        }
        for workorder in workorders
    ]

    return JsonResponse(data, safe=False)


@require_http_methods(["GET"])
def workorder_detail(request, pk):
    workorder = get_object_or_404(WorkOrder, pk=pk)

    data = {
        "id": workorder.id,
        "plate": workorder.plate,
        "vehicle": workorder.vehicle,
        "customer": workorder.customer,
        "customer_phone": workorder.customer_phone,
        "vin": workorder.vin,
        "mileage": workorder.mileage,
        "complaint": workorder.complaint,
        "status": workorder.status,
        "promised_date": (
            workorder.promised_date.isoformat()
            if workorder.promised_date
            else None
        ),
        "check_in": (
            workorder.check_in.isoformat()
            if workorder.check_in
            else None
        ),
        "check_out": (
            workorder.check_out.isoformat()
            if workorder.check_out
            else None
        ),
        "notes": workorder.notes,
        "subtotal": str(workorder.subtotal),
        "total": str(workorder.total),
        "line_items": [
            {
                "id": item.id,
                "quantity": str(item.quantity),
                "description": item.description,
                "unit_price": str(item.unit_price),
                "line_total": str(item.line_total),
                "position": item.position,
            }
            for item in workorder.line_items.all()
        ],
    }

    return JsonResponse(data)


def workorder_create(request):
    workorder = WorkOrder()

    if request.method == "POST":
        form = WorkOrderForm(request.POST, instance=workorder)
        formset = WorkOrderLineItemFormSet(
            request.POST,
            instance=workorder,
        )

        if form.is_valid() and formset.is_valid():
            workorder = form.save()
            formset.instance = workorder
            formset.save()

            messages.success(
                request,
                f"Work order #{workorder.pk} created.",
            )

            return redirect(
                "workorder-detail-page",
                pk=workorder.pk,
            )
    else:
        form = WorkOrderForm(instance=workorder)
        formset = WorkOrderLineItemFormSet(instance=workorder)

    return render(
        request,
        "board/workorder_form.html",
        {
            "form": form,
            "formset": formset,
            "workorder": workorder,
        },
    )


def workorder_edit(request, pk):
    workorder = get_object_or_404(WorkOrder, pk=pk)

    if request.method == "POST":
        form = WorkOrderForm(request.POST, instance=workorder)
        formset = WorkOrderLineItemFormSet(
            request.POST,
            instance=workorder,
        )

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()

            messages.success(
                request,
                f"Work order #{workorder.pk} updated.",
            )

            return redirect(
                "workorder-detail-page",
                pk=workorder.pk,
            )
    else:
        form = WorkOrderForm(instance=workorder)
        formset = WorkOrderLineItemFormSet(instance=workorder)

    return render(
        request,
        "board/workorder_form.html",
        {
            "form": form,
            "formset": formset,
            "workorder": workorder,
        },
    )


def workorder_detail_page(request, pk):
    workorder = get_object_or_404(
        WorkOrder.objects.prefetch_related("line_items"),
        pk=pk,
    )

    return render(
        request,
        "board/workorder_detail.html",
        {
            "workorder": workorder,
        },
    )


def rental_create(request):
    rental = RentalAgreement()

    if request.method == "POST":
        form = RentalAgreementForm(request.POST, instance=rental)

        if form.is_valid():
            rental = form.save()
            messages.success(
                request,
                f"Rental contract #{rental.pk} created.",
            )
            return redirect(
                "rental-detail",
                pk=rental.pk,
            )
    else:
        form = RentalAgreementForm(instance=rental)

    return render(
        request,
        "board/rental_form.html",
        {
            "form": form,
            "rental": rental,
        },
    )


def rental_edit(request, pk):
    rental = get_object_or_404(RentalAgreement, pk=pk)

    if request.method == "POST":
        form = RentalAgreementForm(request.POST, instance=rental)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                f"Rental contract #{rental.pk} updated.",
            )
            return redirect(
                "rental-detail",
                pk=rental.pk,
            )
    else:
        form = RentalAgreementForm(instance=rental)

    return render(
        request,
        "board/rental_form.html",
        {
            "form": form,
            "rental": rental,
        },
    )


def rental_detail(request, pk):
    rental = get_object_or_404(
        RentalAgreement.objects.select_related("rental_car"),
        pk=pk,
    )

    template_name = (
        "board/rental_contract_it.html"
        if rental.language == "IT"
        else "board/rental_contract_en.html"
    )

    return render(
        request,
        template_name,
        {
            "rental": rental,
        },
    )
