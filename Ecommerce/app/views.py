from django.shortcuts import render,redirect,HttpResponse
from .models import Product,Product_category,Customer,Cart,Order
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage
import random

def home(request):
    data=Product.objects.all()
    return render(request,"index.html",{'data':data})

def signup(request):
    return render(request, 'signup.html')

def signupDataSave(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    image = request.FILES.get('image')
    password = request.POST.get('password')

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
        verification_code = str(random.randint(100000, 999999))
        subject = 'Easykart verification code'
        message = 'Your Verification Code is ' + verification_code
        from_email = 'acestechnologypvtltd@gmail.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        image_url = fs.url(filename)
        

        request.session['name'] = name
        request.session['email'] = email
        request.session['phone'] = phone
        request.session['address'] = address
        request.session['image'] = image_url 
        request.session['password'] = password
        request.session['verification_code'] = verification_code
        
        msg = 'Otp sent to your email'
        return render(request, 'otp-verification-register.html', {'error': msg})

def verify_register_otp(request):
    user_entered_otp = request.POST.get('otp')
    email_otp = request.session.get('verification_code')
    name = request.session.get('name')
    email = request.session.get('email')
    phone = request.session.get('phone')
    address = request.session.get('address')
    image = request.session.get('image')
    password = request.session.get('password')

    if user_entered_otp == email_otp:
        Customer.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address,
            image=image,
            password=password
        )
        msg = 'Register successfully!'
        return render(request, 'login.html', {'error': msg})
    else:
        msg = 'Invalid OTP!'
        return render(request, 'otp-verification-register.html', {'error': msg})
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
        return render(request, 'index.html', {'customer': customer})

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
    if request.method=="POST":
        username=request.POST.get('username')
        customer=Customer.objects.filter(email=username).first() or \
            Customer.objects.filter(phone=username).first()
        if customer:
            email=customer.email
            verification_code=str(random.randint(100000, 999999))
            subject = 'Easykart verification code'
            message = 'Your Verification Code is '+verification_code
            from_email = 'acestechnologypvtltd@gmail.com'
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list,fail_silently=False)
            request.session['verification_code'] = verification_code
            request.session['username'] = username
            msg='Otp send Your Email'
            return render(request, 'otp-verification.html',{'error':msg})
    else:
        msg="This email is not registered"
        return render(request,'otp-email.html',{'error':msg})
       
def verify_otp(request):
    user_entered_otp = request.POST.get('otp')
    user_send_otp = request.session.get('verification_code')
    username=request.session.get('userinput')
    if user_entered_otp == user_send_otp:
        request.session['setpassword']=username
        msg='OTP verified successfully!'
        return render(request,'new-password.html',{'error':msg})
    else:
        msg='Invalid OTP!'
        return render(request,'otp-verification.html',{'error':msg})

def changepassword(request):
    userdata=request.session.get('setpassword')
    passwordSave=Customer.objects.get(id=userdata)
    passwordSave.password=request.POST.get('npassword')
    passwordSave.save()
    msg='Password Successfully Changed'
    return render(request,'login.html',{'error':msg})