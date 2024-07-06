from django.urls import path
from . import views
from django.conf.urls.static import static
from ecomm import settings

urlpatterns = [  
    path('about',views.about),
    path('contact',views.contact),
    path('product',views.product),
    path('', views.home1, name='home1'),
    path('home',views.home),
    path('pdetails/<pid>',views.product_details),
    path('register',views.register),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    path('range',views.range),
    path('addtocart/<pid>',views.addtocart),
    path('viewcart',views.viewcart),
    path('remove/<cid>',views.remove),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
    path('makepayment',views.makepayment),
    path('sendmail/<uemail>',views.sendusermail),
    # path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),


]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,
                     document_root=settings.MEDIA_ROOT)
    