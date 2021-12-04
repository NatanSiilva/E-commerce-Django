from django.urls import path
from . import views

app_name = 'order'


urlpatterns = [
	path('', views.Pay.as_view(), name='pay'),
	path('closeorder/', views.CloseOrder.as_view(), name='closeorder'),
	path('list/', views.ListOrders.as_view(), name='list'),
	path('details/', views.Details.as_view(), name='details'),
]
