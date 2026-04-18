from django.urls import path
from . import views

app_name = "dj_control_room_base"

urlpatterns = [
    path("", views.index, name="index"),
    path("examples/", views.examples, name="examples"),
]
