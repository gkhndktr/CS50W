from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:file_name>", views.title, name="file_name"),
    path("Search", views.query, name="query"),
    path("New", views.create, name="create"),
    path("Edit/<str:file_name>", views.edit, name="edit"),
    path("Bring", views.bring, name="bring"),

]

