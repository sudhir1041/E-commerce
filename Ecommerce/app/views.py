from django.shortcuts import render, redirect, HttpResponse
from .models import Product, Product_category, Customer, Cart, Order
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage
import random

def home(request):
    product_details = []
    total_quantity_product = []
    total_quantity = 0
    product_data = Product.objects.all()
    for item in product_data:
        product_details.append({
            'product_name': item.product_name,
            'product_price': item.product_price,
            'product_discount_price': item.product_price - item.product_discount_price,
            'product_description' : item.product_description,
            'product_category' : item.product_category,
            'product_image' : item.product_image,
            'id': item.id
        })
    
    quantity_product = Cart.objects.all()
    for tquantity in quantity_product:
        total_quantity_product.append({
            'quantity': tquantity.quantity
        })
        total_quantity += tquantity.quantity  
        request.session['cart_quantity'] = total_quantity
    print(total_quantity_product)
    print(f'Total Quantity: {total_quantity}')
    categories = Product_category.objects.all()

    return render(request, "index.html", {'product_data': product_details, 'categories': categories, 'total_quantity': total_quantity})

def product_view(request):
    product = Product.objects.all()
    request.session['product_view_session'] = product
    return render(request, 'product_view.html', {'product_view': product})

def cart(request):
    user_email = request.session.get('user_email')
    if not user_email:
        return redirect('login')  

    customer = Customer.objects.filter(email=user_email).first()
    if not customer:
        return redirect('login')  

    cart_items = Cart.objects.filter(customer=customer)
    cart_details = []
    total_price = 0
    total_quantity=0

    for item in cart_items:
        total_discount = item.product.product_price-item.product.product_discount_price
        total = total_discount* item.quantity
        cart_details.append({
            'product_name': item.product.product_name,
            'product_price': item.product.product_price,
            'product_discount_price': item.product.product_price-item.product.product_discount_price,
            'quantity': item.quantity,
            'total': total,
            'id': item.id
        })
        total_price += total
        total_quantity = request.session.get('cart_quantity')
    return render(request, 'cart.html', {'cart_items': cart_details, 'total_price': total_price,'total_quantity': total_quantity})
def remove_from_cart(request, id):
    user_email = request.session.get('user_email')
    if not user_email:
        return redirect('login')  

    customer = Customer.objects.filter(email=user_email).first()
    if not customer:
        return redirect('login')  

    cart_item = Cart.objects.filter(id=id, customer=customer).first()
    if cart_item:
        cart_item.delete()

    return redirect('cart')

def product_category(request, id):
    category = Product_category.objects.get(id=id)
    products = Product.objects.filter(product_category=category)
    return render(request, 'category.html', {'category': category, 'products': products})
def add_to_cart(request, id):
    user_email = request.session.get('user_email')
    if not user_email:
        return redirect('login')  

    product = Product.objects.filter(id=id).first()
    if not product:
        return redirect('/')  

    customer = Customer.objects.filter(email=user_email).first()
    if not customer:
        return redirect('login')  

    cart_item, created = Cart.objects.get_or_create(customer=customer, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('/') 
def product_detail(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    if not product:
        return render(request, 'product_not_found.html')
    total_quantity = request.session.get('cart_quantity')
    return render(request, 'product_detail.html', {'product': product,'total_quantity':total_quantity})
def buy_now(request, product_id):
    
    return HttpResponse("Buy Now feature is under construction.")
# Customer Registration 
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

# Customer Login Page
def login(request):
    return render(request, 'login.html')

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
        return redirect('/')

def profile(request):
    user_email = request.session.get('user_email')
    if not user_email:
        return redirect('/login')
    else:
        total_quantity = request.session.get('cart_quantity')
        customer = Customer.objects.get(email=user_email)
        return render(request, 'profile.html', {'customer': customer,'total_quantity':total_quantity})

def send_email(request):
    return render(request, 'otp-email.html')

def send_otp(request):
    username = request.POST.get('username')
    customer = Customer.objects.filter(email=username).first() or \
        Customer.objects.filter(phone=username).first()
    if not customer:
        msg = "This email is not registered"
        return render(request, 'otp-email.html', {'error': msg})    
    else:
        email = customer.email
        verification_code = str(random.randint(100000, 999999))
        subject = 'Easykart verification code'
        message = 'Your Verification Code is ' + verification_code
        from_email = 'acestechnologypvtltd@gmail.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        request.session['verification_code'] = verification_code
        request.session['username'] = username
        msg = 'Otp sent to your email'
        return render(request, 'otp-verification.html', {'error': msg})

def verify_otp(request):
    user_entered_otp = request.POST.get('otp')
    user_send_otp = request.session.get('verification_code')
    userdata = request.session.get('username')
    if user_entered_otp == user_send_otp:
        request.session['setpassword'] = userdata
        msg = 'OTP verified successfully!'
        return render(request, 'new-password.html', {'error': msg})
    else:
        msg = 'Invalid OTP!'
        return render(request, 'otp-verification.html', {'error': msg})

def changepassword(request):
    usersetdata = request.session.get('setpassword')
    print(usersetdata)
    passwordSave = Customer.objects.get(email=usersetdata) or \
        Customer.objects.get(phone=usersetdata)               
    passwordSave.password = request.POST.get('npassword')
    passwordSave.save()
    msg = 'Password Successfully Changed'
    return render(request, 'login.html', {'error': msg})

def logout(request):
    if 'user_email' in request.session:
        del request.session['user_email']
    return redirect('/login')
