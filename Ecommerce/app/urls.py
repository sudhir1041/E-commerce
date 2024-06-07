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
]
