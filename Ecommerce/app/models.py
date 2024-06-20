from django.db import models

# Create your models here.
class Customer(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField()
    phone=models.IntegerField()
    address=models.CharField(max_length=200)
    image=models.ImageField(upload_to="customer_image/", blank=True, null=True)
    password=models.CharField(max_length=15)

    def __str__(self):
        return self.email
    
class Product_category(models.Model):
    category_name=models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_name=models.CharField(max_length=50)
    product_price=models.FloatField(default=0.0)
    product_discount_price=models.FloatField(default=0.0)
    product_description=models.CharField(max_length=300)
    product_category=models.ForeignKey(Product_category,on_delete=models.CASCADE)
    product_image=models.ImageField(upload_to="product_image/")

    def __str__(self):
        return self.product_name

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.customer.name
STATUS_CHOICES = [
        ('Ordered', 'Ordered'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Packed', 'Packed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
class Order(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Ordered')

    def __str__(self):
        return f"{self.customer.name} - {self.product.product_name} - {self.get_status_display()}"