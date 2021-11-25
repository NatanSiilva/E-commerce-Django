from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [ 
    path('', views.CreateProfile.as_view(), name='create'), 
    path('update/', views.UpdateProfile.as_view(), name='update'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
]
