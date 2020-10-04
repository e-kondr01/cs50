from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView

from .models import *


class ListingList(ListView):
    model = Listing
    template_name = "auctions/index.html"


class WatchListList(LoginRequiredMixin, ListView):
    model = Listing
    template_name = 'auctions/watchlist.html'

    def get_queryset(self):
        w = self.request.user.watchlist
        return w.items.all()


class CreateListing(LoginRequiredMixin, CreateView):
    model = Listing
    fields = ['title', 'description', 'starting_bid', 'image_url',
              'category']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ListingDetail(DetailView):
    model = Listing


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            watchlist = WatchList(owner=user)
            watchlist.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def add_to_watchlist(request, pk):
    watchlist = request.user.watchlist
    watchlist.items.add(Listing.objects.get(pk=pk))
    return HttpResponseRedirect(reverse('listing_detail', kwargs={'pk': pk}))


def remove_from_watchlist(request, pk):
    watchlist = request.user.watchlist
    watchlist.items.remove(Listing.objects.get(pk=pk))
    return HttpResponseRedirect(reverse('listing_detail', kwargs={'pk': pk}))


def new_bid(request, pk):
    if request.method == 'POST':
        bid = Bid.objects.create(bidder=request.user,
                                 listing=Listing.objects.get(pk=pk),
                                 value=request.POST['bid_value'])
        bid.save()
        return HttpResponseRedirect(reverse('listing_detail', kwargs={'pk': pk}))
    else:
        return HttpResponseRedirect(reverse('listing_detail', kwargs={'pk': pk}))
