from django.urls import path
from home import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name="index"),
    # path('products', views.product, name="product"),
    path('contact', views.contact, name="contact"),
    path('about', views.about, name="about"),
    path('profile', views.profile, name="profile"),
    path('tracker', views.tracker, name="tracker"),
    path('cart/', views.cart, name="cart"),
    path('thankyou/', views.thankyou, name="thankyou"),
    path('contactus/', views.contactus, name="contactus"),
    path('handlerequest/', views.handlerequest, name="HandleRequest"),
    path('signup/', views.signup, name='signup'),
    path('login/', views.handlelogin, name='handlelogin'),
    path('logout/', views.handlelogout, name='handlelogout'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-quantity/<int:product_id>/', views.update_quantity, name='update_quantity'),
    path('removefromcart/<int:product_id>/', views.remove_from_cart, name="removefromcart"),
    path('buy_now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('buy_cart/', views.buy_cart, name='buy_cart'),
]
