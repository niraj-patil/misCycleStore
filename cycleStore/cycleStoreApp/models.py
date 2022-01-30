from email.headerregistry import Address
from django.db import models

Gender=(
        ('F','Female'),
        ('M','Male'),
        ('O','Other'))
Order_Status=(
    ('processing','Processing'),
    ('Shipment','Shipment Scheduled'),
    ('Shipped','Shipped'),
    ('delivered','out of delivery'),
    ('canclled','cancle')
    )

# Create your models here.
class Product(models.Model):
    Id              =models.IntegerField(primary_key=True)
    title           = models.CharField(max_length=120)
    description     = models.TextField()
    price           = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    quantity        = models.IntegerField()
    image           = models.ImageField(upload_to='static', null=True, blank=True)
    featured        = models.BooleanField(default=False)
    active          = models.BooleanField(default=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

class Address(models.Model):
    address_line_1  = models.CharField(max_length=120)
    address_line_2  = models.CharField(max_length=120, null=True, blank=True)
    city            = models.CharField(max_length=120)
    country         = models.CharField(max_length=120, default='INDIA')
    state           = models.CharField(max_length=120)
    postal_code     = models.CharField(max_length=120)


class Customer(models.Model):
    Id              =models.IntegerField(primary_key=True)
    Name            =models.CharField(max_length=20)
    billingAddress  =models.ForeignKey(Address,on_delete=models.CASCADE)
    age             =models.IntegerField()
    Gender          =models.CharField(max_length=1,choices=Gender)
    Email           =models.EmailField(max_length=50)


class Order(models.Model):
    Id              =models.IntegerField(primary_key=True)
    ProductID       =models.ForeignKey(Product,on_delete=models.CASCADE)
    Buyer           =models.ForeignKey(Customer,on_delete=models.DO_NOTHING)
    ShippingAddress =models.ForeignKey(Address,on_delete=models.CASCADE)
    Status          =models.CharField(max_length=15,choices=Order_Status)
    TrasactionID    =models.CharField(max_length=50)
    timestamp       = models.DateTimeField(auto_now_add=True)

class Cart(models.Model):
    user        = models.ForeignKey(Customer, null=True, blank=True,on_delete=models.CASCADE)
    products    = models.ManyToManyField(Product, blank=True)
    subtotal    = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total       = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    total1      = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)