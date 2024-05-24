from django.shortcuts import render,redirect,HttpResponse
from .models import Product,Product_category,Customer,Cart,Order

def home(request):
    data=Product.objects.all()
    return render(request,"index.html",{'data':data})

def signup(request):
    return render(request,'signup.html')

def login(request):
    return render(request,'login.html')

def profile(request):
    return render(request,'profile.html')

def logout(request):
    return HttpResponse("successfuly Logout")