from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django import forms
from .models import User,Listing,Category,Bid,Comment,Watchlist
from django.views.generic import DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'

def index(request):
    #Get all listing 
    listings = Listing.objects.all()
    return render(request, "auctions/index.html",{
        'auctions':listings
    })

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

class NewListingForm(forms.Form):
    categories = Category.objects.all()
    name = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea)
    image=forms.ImageField()
    price = forms.FloatField(label='Initial Price')
    category = forms.ModelChoiceField(queryset=categories)


def newListing(request):
    if(request.method=='POST'):
        form = NewListingForm(request.POST,request.FILES)
        if(form.is_valid()):
            name=form.cleaned_data['name']
            description=form.cleaned_data['description']
            price = float(form.cleaned_data['price'])
            category = Category.objects.get(pk=form.cleaned_data['category'].id)
            image = request.FILES['image']
            listing = Listing.objects.create(name=name,description=description,price=price,
                              category=category,image=image,user = request.user,active=True)
            listing.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request,'auctions/newListing.html',{'form':form})
    else:
        return render(request,'auctions/newListing.html',{'form':NewListingForm()})

def itemDetail(request,item_name):
    if(request.method=='POST'):
        listing = Listing.objects.get(name=item_name)
        #check if it's already in his watchlist
        try:
            watchlist = Watchlist.objects.get(user=request.user,listing=listing)
        except ObjectDoesNotExist:
            watchlist = Watchlist.objects.create(user=request.user,listing=listing)
            watchlist.save()
    try:
        item = Listing.objects.get(name=item_name)
        return render(request,'auctions/itemDetail.html',{'item':item})
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('index'))
    
def listCategories(request):
    categories = Category.objects.all()
    return render(request,'auctions/listCategories.html',{'categories':categories})

def itemByCategory(request,category):
    category = Category.objects.get(name=category)
    listings = category.listing_set.all()
    return render(request,'auctions/index.html',{'auctions':listings})

@login_required
def listWatchlist(request):
    try:
        user = request.user
        listings = [watchlist.listing for watchlist in user.watchlist_set.all()]
        return render(request,'auctions/index.html',{
            'auctions':listings,
            'text':f'Watchlist for {user.username}'})
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('index'))