from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:title>/', views.wiki_entry, name='wiki_page'),
    path('random/', views.random, name='random'),
    path('search/', views.search, name='search'),
    path('new_page/', views.new_page, name='new_page'),
    path('create_page/', views.create_page, name='create_page'),
    path('edit_page/<str:title>/', views.edit_page, name='edit_page'),
    path('save_edited/', views.save_edited, name='save_edited'),
    
]
