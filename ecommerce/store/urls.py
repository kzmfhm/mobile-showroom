from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('catalog/<int:company_id>/', views.catalog, name='catalog'),
    path('car_detail/<int:product_id>/', views.car_detail, name='car_detail'),
]
