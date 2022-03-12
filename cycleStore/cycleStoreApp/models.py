from email.headerregistry import Address
from subprocess import CompletedProcess
from django.db import models

GENDER=(
        ('F','Female'),
        ('M','Male'),
        ('O','Other')
        )
ORDER_STATUS=(
    ('processing','Processing'),
    ('shipment','Shipment Scheduled'),
    ('shipped','Shipped'),
    ('delivered','Out for Delivery'),
    ('cancelled','Cancel')
    )
AGE_GROUP=(
    ('0 to 14','Below 14'),
    ('15 to 23','15 to 23'),
    ('24 to 36','24 to 36'),
    ('36+','Above 36')
)
FINANCE=(
    ('-','Debit'),
    ('+','Credit'),
    ('~','Values')
)


# Create your models here.
class Colour(models.Model):
    colour          = models.CharField(max_length=20,primary_key=True)
class Type(models.Model):
    type            = models.CharField(max_length=20,primary_key=True)
class Product(models.Model):
    ID              = models.AutoField(primary_key=True)
    title           = models.CharField(max_length=120)
    description     = models.TextField()
    image           = models.ImageField(upload_to='static', null=True, blank=True)
    featured        = models.BooleanField(default=False)
    active          = models.BooleanField(default=True)
    sales           = models.PositiveIntegerField(default=0)
    profit          = models.DecimalField(decimal_places=2, max_digits=30,default=0)
    timestamp       = models.DateTimeField(auto_now_add=True,auto_now=False)
    
class UniqueProduct(models.Model):
    product         =models.ForeignKey(Product,on_delete=models.CASCADE)
    type            =models.ForeignKey(Type,on_delete=models.CASCADE)
    colour          =models.ForeignKey(Colour,on_delete=models.CASCADE)
    profitPerItem   =models.DecimalField(decimal_places=2, max_digits=20,default=1000)
    sales           =models.IntegerField(default=0)
    price           =models.DecimalField(decimal_places=2, max_digits=20, default=4999)
    quantity        =models.PositiveIntegerField(default=50)
    profit          =models.DecimalField(decimal_places=2, max_digits=20,default=0)
    
    def save(self, *args, **kwargs):
        self.profit=self.sales * self.profitPerItem
        super().save(*args, **kwargs)
    
class Address(models.Model):
    address_line_1  = models.CharField(max_length=120)
    address_line_2  = models.CharField(max_length=120, null=True, blank=True)
    city            = models.CharField(max_length=120)
    country         = models.CharField(max_length=120, default='INDIA')
    state           = models.CharField(max_length=120)
    postal_code     = models.CharField(max_length=120)

class Customer(models.Model):
    ID              =models.AutoField(primary_key=True)
    name            =models.CharField(max_length=20)
    username        =models.CharField(max_length=20)
    password        =models.CharField(max_length=20)
    billingAddress  =models.ForeignKey(Address,on_delete=models.CASCADE,blank=True)
    age             =models.CharField(max_length=8,choices=AGE_GROUP)
    gender          =models.CharField(max_length=1,choices=GENDER)
    email           =models.EmailField(max_length=50)
    timestamp       =models.DateTimeField()   #models.DateTimeField(auto_now_add=True,auto_now=False)
    
class Order(models.Model):
    ID              = models.AutoField(primary_key=True)
    product         = models.ForeignKey(UniqueProduct,on_delete=models.DO_NOTHING)
    customer        = models.ForeignKey(Customer,on_delete=models.DO_NOTHING)
    shippingAddress = models.ForeignKey(Address,on_delete=models.DO_NOTHING)
    status          = models.CharField(max_length=15,choices=ORDER_STATUS)
    transactionID   = models.CharField(max_length=50)
    timestamp       = models.DateTimeField()    #models.DateTimeField(auto_now_add=True,auto_now=False)


class Employee(models.Model):
    name            = models.CharField(max_length=20)
    salary          = models.IntegerField()
    paid            = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)

class Finances(models.Model):
    id              = models.AutoField(primary_key=True)
    description     = models.CharField(max_length=50)
    amount          = models.IntegerField()
    type            = models.CharField(max_length=1,choices=FINANCE)
    completed       = models.BooleanField(default=False)