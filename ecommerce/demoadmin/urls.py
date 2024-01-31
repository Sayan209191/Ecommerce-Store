from django.urls import path
from demoadmin import views

app_name = 'customadmin'

urlpatterns = [
    path('',views.adminlogin,name="adminlogin"), # type: ignore
    path('dashboard/', views.dashboard, name="dashboard"),
    path('calender', views.calender, name="calender"),
    path('adminlogout/', views.adminlogout, name="adminlogout"), # type: ignore
    path('product/', views.product, name="product"), 
    path('user/', views.user, name="user"),
    path('orders/', views.orders, name="orders"),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('edit_customer/<int:user_id>/', views.edit_customer, name='edit_customer'),
    path('delete_customer/<int:user_id>/', views.delete_customer, name='delete_customer'),
    path('add_product', views.add_product, name="add_product"),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
]
