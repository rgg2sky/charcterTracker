from django.urls import path
from . import views
from .auth_views import register

urlpatterns = [
    path("", views.character_list, name="character_list"),
    path("register/", register, name="register"),

    path("characters/new/", views.character_create, name="character_create"),
    path("characters/<int:character_id>/", views.character_detail, name="character_detail"),
    path("characters/<int:character_id>/edit/", views.character_edit, name="character_edit"),
]