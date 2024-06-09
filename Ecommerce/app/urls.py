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

]
