from django.urls import path

from .views import (
    board_view,
    rental_create,
    rental_detail,
    rental_edit,
    workorder_create,
    workorder_detail,
    workorder_detail_page,
    workorder_edit,
    workorder_list,
)


urlpatterns = [
    path("board/", board_view, name="board"),

    path("work-orders/new/", workorder_create, name="workorder-create"),
    path("work-orders/<int:pk>/", workorder_detail_page, name="workorder-detail-page"),
    path("work-orders/<int:pk>/edit/", workorder_edit, name="workorder-edit"),

    path("rentals/new/", rental_create, name="rental-create"),
    path("rentals/<int:pk>/", rental_detail, name="rental-detail"),
    path("rentals/<int:pk>/edit/", rental_edit, name="rental-edit"),

    path("api/workorders/", workorder_list, name="workorder-list"),
    path("api/workorders/<int:pk>/", workorder_detail, name="workorder-detail"),
]
