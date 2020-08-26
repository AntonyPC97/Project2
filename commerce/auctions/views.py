from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User,Auction,Category
from django.views.generic import DetailView

def index(request):
    #Get all auctions from the logged in user
    if(request.user.id is not None):
        auctions = Auction.objects.filter(user = request.user).all()
        return render(request, "auctions/index.html",{'auctions':auctions})
    else:
        return render(request, "auctions/index.html")


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

class NewAuctionForm(forms.Form):
    categories = Category.objects.all()
    name = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea)
    image=forms.ImageField()
    price = forms.FloatField(label='Initial Price')
    category = forms.ModelChoiceField(queryset=categories)

def newAuction(request):
    if(request.method=='POST'):
        form = NewAuctionForm(request.POST,request.FILES)
        if(form.is_valid()):
            name=form.cleaned_data['name']
            description=form.cleaned_data['description']
            price = float(form.cleaned_data['price'])
            category = Category.objects.get(pk=form.cleaned_data['category'].id)
            image = request.FILES['image']
            auction = Auction.objects.create(name=name,description=description,price=price,
                              category=category,image=image,user = request.user,active=True)
            auction.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request,'auctions/newAuction.html',{'form':form})
    else:
        return render(request,'auctions/newAuction.html',{'form':NewAuctionForm()})