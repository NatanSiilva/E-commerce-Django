from django.urls import path
from . import views

app_name = 'order'


urlpatterns = [
	path('', views.Pay.as_view(), name='pay'),
	path('close-order', views.CloseOrder.as_view(), name='close-order'),
	path('details', views.Details.as_view(), name='details'),
]
