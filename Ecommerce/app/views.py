from django.shortcuts import render, redirect, HttpResponse
from .models import Product, Product_category, Customer, Cart, Order
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage
import random
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from collections import defaultdict

def home(request):
    product_data = Product.objects.all()
    categorized_products = {}

    for item in product_data:
        category_name = item.product_category.category_name
        if category_name not in categorized_products:
            categorized_products[category_name] = []
        categorized_products[category_name].append({
            'product_name': item.product_name,
            'product_price': item.product_price,
            'product_discount_price': item.product_price - item.product_discount_price,
            'product_description': item.product_description,
            'product_category': category_name,
            'product_image': item.product_image,
            'id': item.id
        })

    user_email = request.session.get('user_email')
    customer = Customer.objects.filter(email=user_email).first()
    total_quantity = 0

    if customer:
        quantity_product = Cart.objects.filter(customer=customer)
        total_quantity = sum(item.quantity for item in quantity_product)
        request.session['cart_quantity'] = total_quantity
    else:
        request.session['cart_quantity'] = 0

    categories = Product_category.objects.all()
    return render(request, "index.html", {
        'product_data': categorized_products, 
        'categories': categories, 
        'total_quantity': total_quantity
    })


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
    total_quantity = 0

    for item in cart_items:
        total_discount = item.product.product_price - item.product.product_discount_price
        total = total_discount * item.quantity
        cart_details.append({
            'product_name': item.product.product_name,
            'product_price': item.product.product_price,
            'product_discount_price': item.product.product_price - item.product.product_discount_price,
            'quantity': item.quantity,
            'image': item.product.product_image,
            'total': total,
            'id': item.id
        })
        total_price += total
        total_quantity += item.quantity  
        request.session['cart_quantity'] = total_quantity
        request.session['payment_amount'] = total_price

    return render(request, 'cart.html', {'cart_items': cart_details, 'total_price': total_price, 'total_quantity': total_quantity})

def increment_quantity(request, item_id):
    cart_item = Cart.objects.filter(id=item_id).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')  

def decrement_quantity(request, item_id):
    cart_item = Cart.objects.filter(id=item_id).first()
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart')

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
    categories = Product_category.objects.all()
    return render(request, 'category.html', {'category': category, 'products': products, 'categories':categories})

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
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
def buy_now(request):
    user_email = request.session.get('user_email')
    if not user_email:
        return redirect('/login')

    if request.method == 'POST':
        # Handle the payment confirmation
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        # Verify the payment
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        if razorpay_client.utility.verify_payment_signature(params_dict):
            # Payment successful
            customer = Customer.objects.filter(email=user_email).first()
            cart_items = Cart.objects.filter(customer=customer)
            order_details = []
            for item in cart_items:
                total_price = item.quantity * (item.product.product_price - item.product.product_discount_price)
                order_details.append({
                    'product_name': item.product.product_name,
                    'product_price': item.product.product_price,
                    'product_discount_price': item.product.product_discount_price,
                    'quantity': item.quantity,
                    'product_image': item.product.product_image.url,
                    'total_price': total_price
                })
                Order.objects.create(
                    customer=customer,
                    product=item.product,
                    quantity=item.quantity
                )
                item.delete()

            request.session['cart_quantity'] = 0
            return render(request, 'order_status.html', {'success': 'Order placed and payment successful!', 'order_details': order_details})
        else:
            return render(request, 'order_status.html', {'error': 'Payment verification failed!'})

    else:
        # Display the payment form
        amount = request.session.get('payment_amount', 0)
        currency = 'INR'
        amount = int(amount * 100)

        razorpay_order = razorpay_client.order.create(dict(
            amount=amount,
            currency=currency,
            payment_capture='0'))

        razorpay_order_id = razorpay_order['id']

        context = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_merchant_key': settings.RAZOR_KEY_ID,
            'razorpay_amount': amount,
            'currency': currency,
        }
        return render(request, 'order_confirm.html', context=context)

@csrf_exempt
def place_order(request):
    user_email = request.session.get('user_email')
    if not user_email:
        return redirect('login')  

    customer = Customer.objects.filter(email=user_email).first()
    if not customer:
        return redirect('login')  

    cart_items = Cart.objects.filter(customer=customer)
    if not cart_items.exists():
        return render(request, 'order_status.html', {'error': 'Cart is empty'})

    order_details = []
    for item in cart_items:
        total_price = item.quantity * (item.product.product_price - item.product.product_discount_price)
        order_details.append({
            'product_name': item.product.product_name,
            'product_price': item.product.product_price,
            'product_discount_price': item.product.product_discount_price,
            'quantity': item.quantity,
            'product_image': item.product.product_image.url,
            'total_price': total_price
        })
        Order.objects.create(
            customer=customer,
            product=item.product,
            quantity=item.quantity
        )
        item.delete()

    request.session['cart_quantity'] = 0
    return render(request, 'order_status.html', {'success': 'Order placed successfully!', 'order_details': order_details})
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
        customer = Customer.objects.filter(email=username, password=password).first()
        if not customer:
            customer = Customer.objects.filter(phone=username, password=password).first()
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
        customer = Customer.objects.filter(email=user_email).first()
        latest_order = Order.objects.filter(customer=customer).order_by('-created_at').first()
        total_quantity = request.session.get('cart_quantity')
        return render(request, 'profile.html', {'customer': customer, 'latest_order': latest_order, 'total_quantity':total_quantity})

def cancel_order(request, order_id):
    user_email = request.session.get('user_email')
    if not user_email:
        return redirect('/login')
    customer = Customer.objects.filter(email=user_email).first()
    order = Order.objects.filter(id=order_id, customer=customer).first()
    if order and order.status != 'Cancelled':
        order.status = 'Cancelled'
        order.save()
    return redirect('view_all_orders')

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
    if not usersetdata:
        return redirect('login')
    customer = Customer.objects.filter(email=usersetdata).first()
    if not customer:
        customer = Customer.objects.filter(phone=usersetdata).first()
    if customer:
        customer.password = request.POST.get('npassword')
        customer.save()
        msg = 'Password Successfully Changed'
    else:
        msg = 'User not found'
    return render(request, 'login.html', {'error': msg})

def logout(request):
    if 'user_email' in request.session:
        del request.session['user_email']
    return redirect('/login')

def update_profile(request):

    return render(request, 'update_profile.html')

def edit_address(request):

    return render(request, 'edit_address.html')
def change_password_page(request):
    user_email = request.session.get('user_email')
    if not user_email:
        msg = 'User not found'
        return render(request, 'login.html', {'error': msg})
    else:
        return render(request,'change_password.html')
def change_password(request):
    user_email = request.session.get('user_email')
    if not user_email:
        return redirect('login')
    customer = Customer.objects.filter(email=user_email).first()
    if not customer:
        customer = Customer.objects.filter(phone=user_email).first()
    if customer:
        customer.password = request.POST.get('npassword')
        customer.save()
        msg = 'Password Successfully Changed'
        return redirect('/profile')
    else:
        msg = 'User not found'
    return render(request, 'login.html', {'error': msg})

def view_all_orders(request):
    user_email = request.session.get('user_email')
    if not user_email:
        return redirect('login')
    
    customer = Customer.objects.get(email=user_email)
    orders = customer.order_set.all()
    total_quantity = request.session.get('cart_quantity')
    return render(request, 'view_all_orders.html', {'orders': orders, 'total_quantity':total_quantity})

def search(request):
    query = request.GET.get('query')
    results = []
    if query:
        results = Product.objects.filter(product_name__icontains=query)
        print(results)
    return render(request, 'find_product.html', {'product_data': results, 'query': query})

