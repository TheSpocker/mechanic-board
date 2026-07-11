from django.urls import path

from .views import board_view, workorder_detail, workorder_list

urlpatterns = [
    path("board/", board_view),
    path("api/workorders/", workorder_list, name="workorder-list"),
    path("api/workorders/<int:pk>/", workorder_detail, name="workorder-detail"),
]
