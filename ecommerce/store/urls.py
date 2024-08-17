from django.urls import path
from . import views


urlpatterns = [
    path('', views.company_list, name='store'),
    path('login/', views.login_view, name='login'),
    path('validate_form/', views.validate_form, name='validate_form'),
    path('register/', views.register, name='register'),
    path('catalog/<int:company_id>/', views.catalog, name='catalog'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('car_detail/<int:product_id>/', views.carDetail, name='car_detail'),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('logout/', views.logout_view, name='logout'),
]
