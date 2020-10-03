from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.ListingList.as_view(), name="index"),
    path("login/", auth_views.LoginView.as_view(template_name='auctions/login.html'), name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('listing/create', views.CreateListing.as_view(), name='create_listing'),
    path('listing/<int:pk>/', views.ListingDetail.as_view(), name='listing_detail'),
    path('add_to_watchlist/<int:pk>', views.add_to_watchlist, name='add_to_watchlist'),
    path('watchlist', views.WatchListList.as_view(), name='watchlist')
]
