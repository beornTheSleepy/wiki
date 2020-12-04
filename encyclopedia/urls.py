from django.urls import path

from . import views

urlpatterns = [
    ##path("layout", views.search, name="search"),
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("search/", views.search, name="search"),
    path("new/", views.new_entry, name="new_entry"),
    path("random", views.random_page, name="random"),
    path("edit/<str:title>", views.edit_content, name="edit"),
    ###path("errorcreate", views.create_from_error, name="error_create"),
]
