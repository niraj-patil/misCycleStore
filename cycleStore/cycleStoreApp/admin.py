from django.contrib import admin
from .models import Product,Customer,Address,Order,Cart
# Register your models here.
admin.site.register(Product)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(Cart)
