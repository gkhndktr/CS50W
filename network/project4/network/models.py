from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

class User(AbstractUser):
    following = models.ManyToManyField('User', blank=True,null=True, related_name='followed_by')
    follower = models.ManyToManyField('User', blank=True,null=True,related_name='follow_to')

class Post(models.Model):
    post=models.TextField(max_length=400)
    creationTime=models.DateTimeField(blank=True,default=datetime.datetime.now())
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name="posts")
    likes=models.ManyToManyField(User, blank=True,related_name="liked")
    def serialize(self):
        return {
            "id":self.id,
            "post":self.post,
            "creationTime":self.creationTime.strftime("%b %d %Y, %I:%M %p"),
            "user":self.user.username,
            "likes":self.user.username
        }

"""     def __str__(self):
        return f"Created by: {self.user}"
     """