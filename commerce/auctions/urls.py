from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('newListing',views.newListing,name='newListing'),
    path('item/<int:item_id>',views.itemDetail,name='itemDetail'),
    path('categories',views.listCategories,name='listCategories'),
    path('categories/<str:category>',views.itemByCategory,name='itemByCategory'),
    path('watchlist',views.listWatchlist,name='listWatchlist'),
    path('addToWatchlist/<int:item_id>',views.add_watchlist,name='addToWatchlist'),
    path('removeWatchlist/<int:item_id>',views.removeWatchlist,name='removeWatchlist'),
    path('closeListing/<int:item_id>',views.closeListing,name='closeListing')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
