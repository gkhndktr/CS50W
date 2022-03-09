from django.urls import path

from . import views

urlpatterns = [
    # layout,
    path("", views.index, name="index"),
        # layout,login
        path("login", views.login_view, name="login"),
        # layout
        path("logout", views.logout_view, name="logout"),
        # layout,login,register
        path("register", views.register, name="register"),
    # layout,create
    path("create", views.create, name="create"),
    # index,watchlist
    path("product/<int:productId>", views.productPage, name="product"),
    # layout,Product 
    path("watchlist", views.watchlist, name="watchlist"),
    path("bidding", views.bidding, name="bidding"),
    path("close", views.close, name="close"),
    path("comment", views.commenting, name="commenting"),
    path("categories/", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("purchases", views.purchases, name="purchases")
]
