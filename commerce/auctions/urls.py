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
    path('item/<str:item_name>',views.itemDetail,name='itemDetail'),
    path('categories',views.listCategories,name='listCategories'),
    path('categories/<str:category>',views.itemByCategory,name='itemByCategory'),
    path('watchlist',views.listWatchlist,name='listWatchlist')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
