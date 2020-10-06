from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.urls import reverse


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    starting_bid = models.DecimalField(decimal_places=2, max_digits=15)
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='listings')
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.PROTECT,
                               related_name='winner', null=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('listing_detail', kwargs={'pk': self.pk})

    def highest_bidder(self):
        highest_bid = Bid.objects.filter(listing=self).order_by('-value')
        if highest_bid:
            return highest_bid[0].bidder
        else:
            return None

    def current_price(self):
        highest_bid = Bid.objects.filter(listing=self).order_by('-value')
        if highest_bid:
            return highest_bid[0].value
        else:
            return None


class ListingComment(models.Model):
    original_listing = models.ForeignKey(Listing, on_delete=models.CASCADE,
                                         related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments')
    rating = models.IntegerField(default=1)
    posted = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        s = f'On {self.original_listing} by {self.author} with {self.rating}'
        return s


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='bids')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,
                                related_name='bids')
    value = models.DecimalField(decimal_places=2, max_digits=15)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.bidder} {self.value}'


class WatchList(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Listing)

    def __str__(self) -> str:
        return f"{self.owner}'s watchlists"
