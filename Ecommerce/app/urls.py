from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('signup', signup, name='signup'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('signupDataSave',signupDataSave,name='signupDataSave'),
    path('dashboard',dashboard,name='dashboard'),
    path('loginData',loginData,name='loginData'),
    path('profile',profile,name='profile'),
    path('send_email',send_email,name='send_email'),
    path('send_otp',send_otp,name='send_otp'),
    path('verify_otp',verify_otp,name='verify_otp'),
    path('verify_register_otp',verify_register_otp,name='verify_register_otp'),
    path('changepassword',changepassword,name='changepassword'),
    path('category/<int:id>/',product_category, name='product_category'),
    path('cart/', cart, name='cart'),
    path('remove-from-cart/<int:id>/',remove_from_cart, name='remove_from_cart'),
    path('add-to-cart/<int:id>/', add_to_cart, name='add_to_cart'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('buy-now/<int:product_id>/', buy_now, name='buy_now'),

]
