from django.shortcuts import render,redirect,HttpResponse
from .models import Product,Product_category,Customer,Cart,Order
from django.core.mail import send_mail
import random

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
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        customer = Customer.objects.filter(email=username, password=password).first() or \
                   Customer.objects.filter(phone=username, password=password).first()
        
        if customer:
            request.session['user_email'] = customer.email
            return redirect('/dashboard')
        else:
            msg = "Incorrect email/phone and password"
            return render(request, 'login.html', {'error': msg})
    else:
        return redirect('/login')
def dashboard(request):
    user_email = request.session.get('user_email')
    if not user_email:
        return redirect('/login')
    else:
        customer = Customer.objects.get(email=user_email)
        return render(request, 'dashboard.html', {'customer': customer})

def profile(request):
    user_email = request.session.get('user_email')
    if not user_email:
        return redirect('/login')
    else:
        customer = Customer.objects.get(email=user_email)
        return render(request, 'profile.html', {'customer': customer})

def logout(request):
    del request.session['user_email']
    return redirect('/login')

def send_email(request):
    return render(request,'otp-email.html')

def send_otp(request):
    email=request.POST.get('email')
    customer_email=Customer.objects.filter(email=email).first()
    if customer_email:
        verification_code=str(random.randint(100000, 999999))
        subject = 'Easykart verification code'
        message = 'Your Verification Code is '+verification_code
        from_email = 'acestechnologypvtltd@gmail.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list,fail_silently=False)
        request.session['verification_code'] = verification_code
        return render(request, 'otp-verification.html')
    else:
        msg="This email is not registered"
        return render(request,'login.html',{'error':msg})
def verify_otp(request):
    user_entered_otp = request.POST.get('otp')
    user_send_otp = request.session.get('verification_code')
    if user_entered_otp == user_send_otp:
        msg='OTP verified successfully!'
        return render(request,'login.html',{'error':msg})
    else:
        msg='Invalid OTP!'
        return render(request,'otp-verification.html',{'error':msg})
        