#from django.contrib import admin
#from backendTestApp import models
# Register your models here.

#class ProductAdmin(admin.ModelAdmin):
#    list_display=('productID','name')
    
from django.contrib import admin
from .models import *

#AdminPage Displays
class ProductAdmin(admin.ModelAdmin):
    list_display=('ID','title','sales','active','profit')
class UniqueProductAdmin(admin.ModelAdmin):
    list_display=('product','type','colour','price','quantity','profitPerItem','sales','profit')
class AddressAdmin(admin.ModelAdmin):
    list_display=('id','city','country','postal_code')
class OrderAdmin(admin.ModelAdmin):
    list_display=('ID','shippingAddress','transactionID','timestamp')
class CustomertAdmin(admin.ModelAdmin):
    list_display=('ID','name','email','age','gender')
class ColourAdmin(admin.ModelAdmin):
    list_display=('colour',)
class TypeAdmin(admin.ModelAdmin):
    list_display=('type',)
    

# Register your models here.
admin.site.register(Product,ProductAdmin)
admin.site.register(UniqueProduct,UniqueProductAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Customer,CustomertAdmin)
admin.site.register(Colour,ColourAdmin)
admin.site.register(Type,TypeAdmin)
admin.site.register(Employee)
admin.site.register(Finances)