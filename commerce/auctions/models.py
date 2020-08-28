from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Listing(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField()
    date_listed = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='uploads/')
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} by {self.user}"

class Bid(models.Model):
    bid = models.FloatField()
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    winner = models.BooleanField(default=False)

    def __str__(self):
        return f'Bid of {round(self.bid,2)} place by {self.user.username} on item {self.listing.id}'

class Comment(models.Model):
    comment = models.TextField()
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date_comment = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} commented on item {self.listing.id}'

class Watchlist(models.Model):
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} watchlist item {self.listing.id}'