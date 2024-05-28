from django.shortcuts import render,redirect,HttpResponse
from .models import Product,Product_category,Customer,Cart,Order

def home(request):
    data=Product.objects.all()
    return render(request,"index.html",{'data':data})

def signup(request):
    return render(request,'signup.html')
def signupDataSave(request):
    name=request.POST.get('name')
    email=request.POST.get('email')
    phone=request.POST.get('phone')
    address=request.POST.get('address')
    image = request.FILES.get('image')
    password=request.POST.get('password')
    if len(password) < 8:
        msg = "Password too short. Please enter at least 8 characters."
        return render(request, 'signup.html', {'error': msg})
    elif Customer.objects.filter(email=email).exists():
        msg = "This email ID already exists."
        return render(request, 'signup.html', {'error': msg})
    elif Customer.objects.filter(phone=phone).exists():
        msg = "This phone number already exists."
        return render(request, 'signup.html', {'error': msg})
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

def loginData(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        try:
            customer = Customer.objects.get(email=email, phone=phone)
        except Customer.DoesNotExist:
            msg = "Invalid email or phone number."
            return render(request, 'login.html', {'error': msg})
    
        if customer.password != password:
            msg = "Invalid password."
            return render(request, 'login.html', {'error': msg})
        
        request.session['user_email'] = customer.email
        return redirect('/dashboard')
    
    return redirect('/login')

def profile(request):
    return render(request,'profile.html')

def logout(request):
    request.session.flush()
    return redirect('/login')