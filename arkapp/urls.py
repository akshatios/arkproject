
from django.urls import path,include
from arkapp import views
from . import views

urlpatterns = [
    path('',views.home,name='index'),
    path('checkout/', views.checkout, name='checkout'),
    path('purchase/', views.purchase, name='purchase'),
]