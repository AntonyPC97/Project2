from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Auction(models.Model):
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