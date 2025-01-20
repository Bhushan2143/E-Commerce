from django.urls import path,include
from ecomapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register',views.register),
    path('login',views.user_login),
    path('product',views.product),
    path('logout',views.user_logout),
    path('catfilter/<cv>',views.catfilter),
    path('sortfilter/<sv>',views.sortfilter),
    path('pricefilter',views.pricefilter),
    path('product_detail',views.product_detail),
    path('placeorder',views.placeorder),
    path('cart',views.cart),
    path('product_detail/<pid>',views.product_detail),
    path('addtocart/<pid>',views.addtocart),
    path('cart',views.cart),
    path('updateqty/<x>/<cid>',views.updateqty), 
    path('remove/<cid>',views.remove),
    path('placeorder',views.placeorder),
    path('fetchorder',views.fetchorder),
    path('srcfilter',views.srcfilter),
    path('makepayment',views.makepayment),
    path('paymentsuccess',views.paymentsuccess),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)