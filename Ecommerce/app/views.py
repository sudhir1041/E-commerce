from django.shortcuts import render,redirect,HttpResponse
from .models import Product,Product_category,Customer,Cart,Order

def home(request):
    data=Product.objects.all()
    return render(request,"index.html",{'data':data})

def signup(request):
    return render(request,'signup.html')
def signupDataSave(request):
    name=request.POST.get()
    email=request.POST.get()
    phone=request.POST.get()
    address=request.POST.get()
    image = request.FILES.get('image')
    password=request.POST.get()
    if(password>8):
        msg="Password to short Please Enter Min 8 character"
        return render(request,'signup.html',{'error':msg})
    elif Customer.objects.filter(email==email):
        msg="This email id Already Exiest"
        return render(request,'login.html',{'error':msg})
    else:
        Customer.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address,
            image=image,
            password=password
        )
        return redirect('/login')
    
    

def login(request):
    return render(request,'login.html')

def profile(request):
    return render(request,'profile.html')

def logout(request):
    return HttpResponse("successfuly Logout")