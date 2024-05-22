from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('', views.home, name='home'),
]
=======
    path('',home,name="home"),
]
>>>>>>> b718097fcec6015f05785010fc1a60ac98cc2e25
