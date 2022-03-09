from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model
from django.contrib import admin
from django.db.models.fields import NullBooleanField
from django.forms import widgets
from django.utils import timezone


class User(AbstractUser):
    pass



class product(models.Model):
    id = models.BigAutoField(primary_key=True)
    item=models.CharField(max_length=64)
    definition=models.TextField(max_length=400)
    price=models.FloatField(null=True,blank=True)
    creationTime=models.DateTimeField(default=timezone.now)
    creator=models.ForeignKey(User, on_delete=models.CASCADE,related_name="sellers")
    categories=[
        ('Elektronik', 'Elektronik'),
        ('Mobilya', 'Mobilya'),
        ('Fashion', 'Fashion    '),
        ('Sports', 'Sports'),
        ('Hobbies', 'Hobbies'),
        ('No Category', 'No Category'),
    ]
    category=models.CharField(choices=categories,default="No category",max_length=64)
    imageUrl=models.URLField(null=True,blank=True)
    watchlist=models.ManyToManyField(User, blank=True,related_name="watching")
    bidder= models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name="winner" )
    sold=models.BooleanField(default=False)
    def __str__(self):
        return f"Product: {self.item}: By {self.creator}"
    
class bid(models.Model):
    creator=models.ForeignKey(User, on_delete=models.CASCADE,related_name="bidder")
    item=models.ForeignKey(product, on_delete=models.CASCADE, related_name="bidItems",null=True,blank=True)
    price=models.FloatField()
    def __str__(self):
        return f"By {self.creator} for {self.item}"

class comment(models.Model):
    creator=models.ForeignKey(User, on_delete=models.CASCADE,related_name="evaluations")
    item=models.ForeignKey(product, on_delete=models.CASCADE, related_name="comments",null=True,blank=True)
    comment=models.TextField(max_length=400)
    creationTime=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"By {self.creator} about {self.item}"



