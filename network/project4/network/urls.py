
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:profile>", views.profile, name="profile"), 
    path("following", views.following, name="following"),  
    # API Routes
    path("like/<str:id>",views.like, name="like"),
    path("unlike/<str:id>",views.unlike, name="unlike"),
    path("follow/<str:profile>",views.follow, name="follow"),
    path("unfollow/<str:profile>",views.unfollow, name="unfollow"),
    path("edit/<str:id>",views.edit, name="edit")
]
