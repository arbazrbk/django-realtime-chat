from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path("", views.room_list, name="room_list"),
    path("rooms/<slug:slug>/", views.room_detail, name="room_detail"),
]
