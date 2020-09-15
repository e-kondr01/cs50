from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:title>/', views.wiki_entry, name='wiki_page'),
    path('random/', views.random, name='random'),
    path('search/', views.search, name='search'),
]
