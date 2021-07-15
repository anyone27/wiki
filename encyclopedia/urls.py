from django.urls import path

from encyclopedia import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:wiki>", views.wiki, name="wiki"),
    path("search", views.search, name="search"),
    path("new_page", views.new_page, name="new_page"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random_page", views.random_page, name="random_page"),
]
