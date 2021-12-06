from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.ListProduct.as_view(), name='list'),
    path('<slug>', views.DetailsProduct.as_view(), name='details'),
    path('addtocart/', views.AddToCartProduct.as_view(), name='addtocart'),
    path('removefromcart/', views.RemoveFromCartProduct.as_view(),
         name='removefromcart'),
    path('cart/', views.Cart.as_view(), name='cart'),
    path('purchasesummary/', views.PurchaseSummary.as_view(), name='purchasesummary'),
    path('search/', views.Search.as_view(), name='search'),

]
