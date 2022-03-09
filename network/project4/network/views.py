from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import JsonResponse
import json
from network.models import User
from network.models import Post
from django.views.decorators.csrf import csrf_exempt
from network.forms import PostForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

# from django.views.generic import(
#     ListView,
# )
from django.core.paginator import Paginator
# Inside index html there will be a form for post requests. Django's form is may be used for this transactions.
#  I will use form to show it on the page, but for request I will use javaScript fetch.
@csrf_exempt
def index(request):
    if request.method=="POST":
        post = request.POST["postText"]
        entry = Post.objects.create(post=post, user=request.user)
        entry.save()
        return HttpResponseRedirect('/')

    posts = Post.objects.all().order_by('id').reverse()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    if not page_number:
        page_number=1
    posts = paginator.get_page(page_number)
    form = PostForm()
    if request.user.is_authenticated:
        user_likes = User.objects.get(username=request.user).liked.all()
        return render(request, "network/index.html", {"posts": posts, "form": form, "user_likes": user_likes})
    return render(request, "network/index.html", {"posts": posts, "form": form})
def profile(request,profile):
    if request.method=="GET":
        profile=User.objects.get(username=profile)
        posts = Post.objects.filter(user=profile).order_by('id').reverse()
        posts_count=posts.count
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        if not page_number:
            page_number=1
        posts = paginator.get_page(page_number)
        follower=profile.follower.all().count
        following=profile.following.all().count
        if request.user.is_authenticated:
            user=User.objects.get(username=request.user)
            if profile in user.following.all():
                follow_or_not="Unfollow"
            else:
                follow_or_not="Follow"
            # auth
            content={"following":following,"follower":follower,"posts":posts,"profile":profile,"follow_unfollow":follow_or_not,"user":user,"posts_count":posts_count}
            return render(request, "network/profile.html",content)
        # not...
        content={"following":following,"follower":follower,"posts":posts,"profile":profile,"posts_count":posts_count}
        return render(request, "network/profile.html",content)   
def following(request):
    user=User.objects.get(username=request.user)
    following=user.following.all()
    posts = Post.objects.all().order_by('id').reverse()
    paginator = Paginator(posts, 10)
    followins_post=[post for post in posts if post.user in following]
    page_number = request.GET.get('page')
    if not page_number:
        page_number=1
    posts = paginator.get_page(page_number)
    if request.user.is_authenticated:
        user_likes = User.objects.get(username=request.user).liked.all()

        return render(request, "network/following.html", {"posts": followins_post, "user_likes": user_likes})
    return render(request, "network/following.html", {"posts": followins_post})
@login_required
def follow(request,profile):
    if request.method == "GET":
        user=User.objects.get(username=request.user)
        profile=User.objects.get(username=profile)
        user.following.add(profile)
        profile.follower.add(user)
        return JsonResponse({"status": "followed"}, status=201)
@login_required
def unfollow(request,profile):
    if request.method == "GET":
        user=User.objects.get(username=request.user)
        profile=User.objects.get(username=profile)
        user.following.remove(profile)
        profile.follower.remove(user)
        return JsonResponse({"status": "unfollowed"}, status=201)

@login_required
@csrf_exempt
def edit(request,id):

    # model is not updated by the post coming from request...
    if request.method == "PUT":
        entry = Post.objects.get(id=id)
        owner=entry.user
        changer=User.objects.get(username=request.user)
        if owner==changer:
            post = json.loads(request.body)["post"]
            
            entry.post=post
            entry.save()
            return JsonResponse({"post": "post is updated"}, status=201)
        else:
            return JsonResponse({"error": "you are not authorised for this transaction"}, status=401)
@csrf_exempt
def like(request, id):
    if request.method == "PUT":
        user = User.objects.get(username=request.user)
        post = Post.objects.get(id=id)
        post.likes.add(user)
        post.save()
        return JsonResponse({"message": "Your like has been recorded."}, status=201)
@csrf_exempt
def unlike(request, id):
    if request.method == "PUT":
        print("its here")
        user = User.objects.get(username=request.user)
        post = Post.objects.get(id=id)
        post.likes.remove(user)
        post.save()
        return JsonResponse({"message": "Your like has been removed."}, status=201)
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")
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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
