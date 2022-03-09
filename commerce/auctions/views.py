from django.contrib.auth import authenticate, login, logout,get_user
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import createForm
from .models import User
from .models import product
from .models import bid
from .models import comment
from django.contrib.auth.decorators import login_required

def index(request):
    auctions=product.objects.all()
    # One html file is used for index, watchlist and category listing. Index=True makes index page's heading accorging to index.
    index=True
    return render(request, "auctions/index.html", {"auctions":auctions,"index":index,})
@login_required
def create(request):
    if request.method=="GET":
        form=createForm()
        return render(request,"auctions/create.html",{"form":form})
    if request.method=="POST":
        form = createForm(request.POST)
        if form.is_valid:
            entry=product(item=form.data["item"],definition=form.data["definition"],price=form.data["price"],category=form.data["category"], imageUrl=form.data["imageUrl"],creator=get_user(request))
            entry.save()
            return redirect(index)
def productPage(request, productId):
    if request.method=="GET":
        
        if request.user.is_authenticated:
            username=get_user(request).username
            UserObject=User.objects.get(username=username)
            print(UserObject.watching)
            # Below watchlist variable is used in product.html to decide in watclist button must be shown or not
            if UserObject.watching.filter(id=productId):
                watchlist=True
            else:
                watchlist=False

            productObject = product.objects.get(id = productId)
            message=""

            if productObject.sold==True and str(productObject.bidder)==username:
                message="congratulations! You Have Won the Bid!"
            if productObject.sold==True and str(productObject.creator)==username:
                message=f"Product has been sold to {productObject.bidder} successfully"
            if productObject.sold==False and str(productObject.bidder)==username:
                message=f"You gave the highest bid so far. Bidding is ongoing..."

            comments=productObject.comments.all()
            return render(request,"auctions/product.html",{"content":productObject,"watchlist":watchlist,"username":username,"message":message,"comments":comments})
        else:
            productObject = product.objects.get(id = productId)
            watchlist=False
            message=""
            username="Visitor"
            comments=productObject.comments.all()
            return render(request,"auctions/product.html",{"content":productObject,"watchlist":watchlist,"username":username,"message":message,"comments":comments})
def categories(request):
    if request.method=="GET":
        catalog= [i.category for i in product.objects.all()]
        # Below function brings a set of recorded categories
        if "No Category" in catalog:
            catalog= sorted(set(i for i in catalog if i !="No Category"))
            catalog.append("No Category")
        else:
            catalog= sorted(set(catalog))
        return render(request,"auctions/index.html",{"catalog":catalog})
def category(request,category):
    if request.method=="GET":
        auctions=[i for i in product.objects.all() if i.category==category]
        catalog= [i.category for i in product.objects.all()]
     
        if "No Category" in catalog:
            catalog= sorted(set(i for i in catalog if i !="No Category"))
            catalog.append("No Category")
        else:
            catalog= sorted(set(catalog))
        return render(request, "auctions/index.html", {"auctions":auctions,"catalog":catalog})
def watchlist(request):
    username=get_user(request).username
    UserObject=User.objects.get(username=username)
    content=UserObject.watching.all()
    if request.method=="POST":
        if request.POST["func"]=="add":
            productId=request.POST["content_id"]
            productWatchObject=product.objects.get(id=productId).watchlist
            productWatchObject.add(UserObject)
        elif request.POST["func"]=="remove":
            productId=request.POST["content_id"]
            productWatchObject=product.objects.get(id=productId).watchlist
            productWatchObject.remove(UserObject)
    # One html file is used for index, watchlist and category listing. Watclist=True makes index page's heading accorging to watchlist.
    watchlist=True
    username=get_user(request).username
    return render(request, "auctions/index.html", {"auctions":content,"watchlist":watchlist,"username":username})
def bidding(request):
    if request.method=="POST":
        givenPrice=float(request.POST["bidItem"])
        productId=request.POST["content_id"]
        # below is a single row related to product id.
        productObject=product.objects.get(id=productId)
        # below is price field of the above object.
        username=get_user(request).username
        UserObject=User.objects.get(username=username)
        comments=productObject.comments.all()
        if givenPrice>productObject.price:
            productObject.price=givenPrice
            productObject.bidder=UserObject
            productObject.save()           
        # now a record for bid model will be saved.
            bidEntry=bid(creator=UserObject,item=productObject,price=givenPrice)
            bidEntry.save()
            message=f"You have successfully bid for product. Bid has raised to Usd {givenPrice}"
            return render(request,"auctions/product.html",{"content":productObject,"watchlist":watchlist,"message":message,"comments":comments})
        else:
            message="Your bid should be bigger then the current price"
            return render(request,"auctions/product.html",{"content":productObject,"watchlist":watchlist,"message":message,"comments":comments})
def close(request):
    if request.method=="POST":
        username=get_user(request).username
        productId=request.POST["content_id"]
        productObject=product.objects.get(id=productId)
        # winner user object is defined below comment
        productObject.sold=True
        productObject.save()
        return redirect(f'/product/{productId}')
        
        # return render(request,"auctions/product.html",{"content":productObject,"username":username})
def purchases(request):
    if request.method=="GET":
        username=get_user(request).username
        UserObject=User.objects.get(username=username)
        wins=[i for i in product.objects.all() if i.bidder==UserObject and i.sold==True]
        return render(request, "auctions/purchases.html", {"auctions":wins})
def commenting(request):
    if request.method=="POST":
        username=get_user(request).username
        productId=request.POST["content_id"]
        productObject=product.objects.get(id=productId)
        UserObject=User.objects.get(username=username)
        commentEntry=comment(creator=UserObject,item=productObject,comment=request.POST["comment"])
        commentEntry.save()
        return redirect(f'/product/{productId}')
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")
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
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

