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


def index(request):
    #Get all listing 
    user = request.user
    listings = Listing.objects.all()
    if(user.id is not None):
        watchlistItems = [x.listing for x in user.watchlist_set.all()] 
        return render(request, "auctions/index.html",{
            'listings':listings,
            'watchlistItems':watchlistItems
        })
    else:
        return render(request, "auctions/index.html",{
            'listings':listings
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

@login_required(login_url='login')
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

@login_required(login_url='login')
def itemDetail(request,item_id):
    item = Listing.objects.get(pk=item_id)
    bidList = item.bid_set.order_by('bid')
    lastBid = bidList.last()
    user = request.user
    if(bidList.exists()):
        currBid=lastBid.bid
    else:
        currBid=item.price

    if(request.method=='POST'):
        if(request.POST.get('bid')):
            newbid = float(request.POST['bid'])
            if (newbid<=currBid):
                return render(request,'auctions/itemDetail.html',{'item':item,'count':len(bidList),'bid':currBid,'lastBid':lastBid})
            else:
                currBid = round(newbid,2)
                bid = Bid.objects.create(user = user,listing=item,bid=currBid)
                bid.save()
                return render(request,'auctions/itemDetail.html',{'item':item,'count':len(bidList),'bid':currBid,'lastBid':lastBid})
        else:
            text = request.POST.get('comment')
            comment = Comment.objects.create(comment=text,user=user,listing=item)
            comment.save()
            return HttpResponseRedirect(reverse('itemDetail', args=[item.id]))
    else:
        try:
            item = Listing.objects.get(pk=item_id)
            return render(request,'auctions/itemDetail.html',{'item':item,'count':len(bidList),'bid':currBid,'lastBid':lastBid})
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('index'))
    
def listCategories(request):
    categories = Category.objects.all()
    return render(request,'auctions/listCategories.html',{'categories':categories})

def itemByCategory(request,category):
    category = Category.objects.get(name=category)
    listings = category.listing_set.all()
    return render(request,'auctions/index.html',{'listings':listings})

@login_required(login_url='login')
def listWatchlist(request):
    user = request.user
    listings = [watchlist.listing for watchlist in user.watchlist_set.all()]
    return render(request,'auctions/watchlist.html',{
        'listings':listings})

@login_required(login_url='login')
def add_watchlist(request,item_id):
    listings = Listing.objects.all()
    #get current user
    user = request.user
    #get item to add to watchlist
    listing = Listing.objects.get(pk=item_id)
    #check if item is in Watchlist, if not, create it
    watchlist,status = Watchlist.objects.get_or_create(user=user,listing=listing)    
    return HttpResponseRedirect(reverse('index'))

@login_required(login_url='login')
def removeWatchlist(request,item_id):
    user = request.user
    listing = Listing.objects.get(pk=item_id)
    watchlist = Watchlist.objects.get(user=user,listing=listing)
    watchlist.delete()
    return HttpResponseRedirect(reverse('listWatchlist'))

@login_required(login_url='login')
def closeListing(request,item_id):
    item = Listing.objects.get(pk=item_id)
    winner = item.bid_set.order_by('bid').last().user
    bid = Bid.objects.get(user=winner,listing=item)
    item.active =False
    item.save()
    bid.winner = True
    bid.save()
    return HttpResponseRedirect(reverse('itemDetail',args=[item_id]))

@login_required(login_url='login')
def deleteListing(request,item_id):
    item = Listing.objects.get(pk=item_id)
    item.active = False
    item.save()
    return HttpResponseRedirect(reverse('index'))
