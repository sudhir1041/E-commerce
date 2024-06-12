from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('view/<int:product_id>/', product_view, name='product_view'),
    path('cart/', cart, name='cart'),
    path('increment_quantity/<int:item_id>/', increment_quantity, name='increment_quantity'),
    path('decrement_quantity/<int:item_id>/', decrement_quantity, name='decrement_quantity'),
    path('remove_from_cart/<int:id>/', remove_from_cart, name='remove_from_cart'),
    path('category/<int:id>/', product_category, name='product_category'),
    path('add_to_cart/<int:id>/', add_to_cart, name='add_to_cart'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('buy_now/<int:product_id>/', buy_now, name='buy_now'),
    path('place_order/', place_order, name='place_order'),
    path('signup/', signup, name='signup'),
    path('signupDataSave/', signupDataSave, name='signupDataSave'),
    path('verify_register_otp/', verify_register_otp, name='verify_register_otp'),
    path('login/', login, name='login'),
    path('loginData/', loginData, name='loginData'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile, name='profile'),
    path('send_email/', send_email, name='send_email'),
    path('send_otp/', send_otp, name='send_otp'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('changepassword/', changepassword, name='changepassword'),
    path('logout/', logout, name='logout'),

]
