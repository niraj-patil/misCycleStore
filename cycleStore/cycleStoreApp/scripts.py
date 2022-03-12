
from random import randint
from numpy import random
from django.contrib.auth import get_user_model
from .models import *
from datetime import datetime
from zoneinfo import ZoneInfo
import indian_names                         #https://libraries.io/pypi/indian-names
import string



def createAdmin():
    User=get_user_model()
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')

def addColour():
    colours=["Red","Black","White"]
    objects=[]
    for entry in colours:
        object=Colour(colour=entry)
        object.save()
        objects.append(object)
    return objects

def addType():
    type=["Geared","Non-Geared"]
    objects=[]
    for entry in type:
        object=Type(type=entry)
        object.save()
        objects.append(object)
    return objects

def addProduct():
    product=[["Cycle1","cycle1"],["Cycle2","cycle2"],["Cycle3","cycle3"]]
    objects=[]
    for entry in product:
        object=Product(title=entry[0],description=entry[1])
        object.save()
        objects.append(object)
    return objects

def createUniqueProduct(colours,types,products):
    objects=[]
    for product in products:
        f=int(input(f"Create Product {product.title} \n 0:No 1:Yes 2:Break >"))
        if(f==0):
            continue
        elif(f==1):
            for colour in colours:
                f=int(input(f"Create Product {product.title} : {colour.colour} \n 0:No 1:Yes 2:Break>"))
                if(f==0):
                    continue
                elif(f==1):
                    for type in types:
                        f=int(input(f"Create Product {product.title} : {colour.colour} : {type.type} \n 0:No 1:Yes 2:Break>"))
                        if(f==0):
                            continue
                        elif(f==1):
                            price=int(input("Enter Price: "))
                            profit=int(input("Enter Profit:"))
                            object=UniqueProduct(product=product,type=type,colour=colour,price=price,profit=profit)
                            object.save()
                            objects.append(object)
                        else:
                            break
                else:
                    break
        else:
            break
    return objects



def addAddress():
    cityAndCode=[["Mumbai",400001,400002,400003],["Pune",400101,400102,400103],["Banglore",400201,400202]]
    objects=[]
    n=int(input("Enter Number of Addresses:"))
    for i in range(n):
        k=random.choice([0,1,2],p=[0.5,0.29,0.21])
        if k==2:
            _state="Karnataka"
        else:
            _state="Maharashtra"

        if k==0:
            j=random.choice([1,2,3],p=[0.45,0.29,0.26])
        elif k==1:
            j=random.choice([1,2,3],p=[0.30,0.34,0.36])
        else:
            j=random.choice([1,2],p=[0.9,0.1])
        object=Address(address_line_1="address line 1",address_line_2="address_line_2",city=cityAndCode[k][0],state=_state,postal_code=cityAndCode[k][j])
        object.save()
        objects.append(object)
    return objects




def addCustomer(addresses):
    objects=[]
    _datetime=[]
    
    decP=[0.0470,0.0470,0.0296,0.0074,0.0148,00.0296,0.0296,0.0391999999999999,0.0370,0.0296,0.0074,0.0148,00.0296,0.0296,0.0370,0.0370,0.0296,0.0074,0.0148,00.0396,0.0444,0.1111,0.1185,0.037,0.0031,0.0222,0.032,0.032,0.0370,0.0029,0.0022]
    janP=[0.0090,0.0454,0.0363,0.0475000000000001,0.0454,0.0363,0.0090,0.0181,0.0363,0.0363,0.0454,0.0454,0.0363,0.0090,0.0181,0.0363,0.0363,0.0454,0.0454,0.0363,0.0090,0.0181,0.0363,0.0363,0.0454,0.0454,0.0363,0.0090,0.0181,0.0363,0.0363]
    febP=[0.0384,0.0580,0.0580,0.0348,0.0096,0.0192,0.0384,0.0384,0.0480,0.0480,0.0498,0.0096,0.0192,0.0384,0.0384,0.0480,0.0480,0.0348,0.0096,0.0192,0.0384,0.0384,0.0480,0.0480,0.0348,0.0096,0.0192,0.05779999999999975]
    
    hourP=[0.021,0.014,0.012,0.01,0.01,0.013,0.02,0.033,0.041,0.053,0.063,0.061,0.056,0.056,0.055,0.054,0.055,0.056,0.058,0.059,0.061,0.06,0.046,0.0329999999999996696]                                  #https://www.salecycle.com/blog/stats/when-are-people-most-likely-to-buy-online/
    december=int(len(addresses)*33/100)
    january=int(len(addresses)*30/100)
    february=int(len(addresses)*37/100)

    for i in range (december):
        day=random.choice([x for x in range (1,32)],p=decP)
        hour=random.choice([x for x in range (24)],p=hourP)
        _datetime.append(datetime(2021,12,day,hour,randint(0,59),tzinfo=ZoneInfo('Asia/Kolkata')))
    for i in range (january):
        day=random.choice([x for x in range (1,32)],p=janP)
        hour=random.choice([x for x in range (24)],p=hourP)
        _datetime.append(datetime(2022,1,day,hour,randint(0,59),tzinfo=ZoneInfo('Asia/Kolkata')))
    for i in range (february):
        day=random.choice([x for x in range (1,29)],p=febP)
        hour=random.choice([x for x in range (24)],p=hourP)
        _datetime.append(datetime(2022,2,day,hour,randint(0,59),tzinfo=ZoneInfo('Asia/Kolkata')))   
    

    if(len(_datetime)!=len(addresses)):
        for i in range(len(addresses)-len(_datetime)):
            hour=random.choice([x for x in range (24)],p=hourP)
            _datetime.append(datetime(2021,12,26,randint(19,22),randint(0,59),tzinfo=ZoneInfo('Asia/Kolkata')))
    _datetime.sort()
    for i in range (len(addresses)):
        j=random.choice(['0 to 14','15 to 23','24 to 36','36+'],p=[0.22,0.43,0.20,0.15])
        k=random.choice(['F','M','O'],p=[0.32,0.67,0.01])
        if k=='M':
            uname=indian_names.get_first_name(gender='male')
        else:
            uname=indian_names.get_first_name(gender='female')
        name=uname+" "+indian_names.get_last_name()
        mail=(name.lower()+"@email.com").replace(" ", "")
        password=''.join(random.choice(list(string.ascii_lowercase) + list(string.ascii_uppercase)) for i in range(10))
        object=Customer(name=name,username=uname,password=password,billingAddress=addresses[i],age=j,gender=k,email=mail,timestamp=_datetime[i])
        object.save()
        objects.append(object)
    return objects        
       
def addOrders(uniqueProducts,customers):
    objects=[]
    for i in range (len(customers)):
        numberOfOrder=random.choice([0,1,2,3,4],p=[0.25,0.60,0.14,0.005,0.005])
        uniqueProductIds=[x for x in range (1,11)]
        for j in range (numberOfOrder):
            if customers[i].gender=="M":
                if customers[i].age=="0 to 14":
                    product=random.choice(uniqueProducts,p=[0.2,0.1,0.17,0.07,0.1,0.07,0.17,0.07,0.03,0.02])
                elif customers[i].age=="15 to 26":
                    product=random.choice(uniqueProducts,p=[0.18,0.11,0.13,0.05,0.08,0.05,0.16,0.08,0.08,0.08])
                elif customers[i].age=="24 to 36":
                    product=random.choice(uniqueProducts,p=[0.103,0.103,0.069,0.038,0.033,0.034,0.207,0.138,0.172,0.103])
                else:
                    product=random.choice(uniqueProducts,p=[0.065,0.065,0.065,0.095,0.065,0.032,0.129,0.097,0.129,0.258])
            else:
                if customers[i].age=="0 to 14":
                    product=random.choice(uniqueProducts,p=[0.1,0.07,0.17,0.07,0.2,0.1,0.03,0.07,0.17,0.02])
                elif customers[i].age=="15 to 26":
                    product=random.choice(uniqueProducts,p=[0.08,0.05,0.13,0.05,0.18,0.11,0.8,0.08,0.16,0.08])
                elif customers[i].age=="24 to 36":
                    product=random.choice(uniqueProducts,p=[0.033,0.034,0.069,0.038,0.103,0.103,0.172,0.138,0.207,0.103])
                else:
                    product=random.choice(uniqueProducts,p=[0.065,0.032,0.065,0.095,0.065,0.065,0.129,0.097,0.129,0.258])
            status=random.choice(["delivered","cancelled"],p=[0.9999,0.0001])
            object=Order(product=product,customer=customers[i],shippingAddress=customers[i].billingAddress,status=status,transactionID=i,timestamp=customers[i].timestamp)
            object.save()
            objects.append(object)
    return objects




def addData():
    createAdmin()
    colours=addColour()
    types=addType()
    products=addProduct()
    uniqueProducts=createUniqueProduct(colours,types,products)
    addresses=addAddress()
    customers=addCustomer(addresses)
    orders=addOrders(uniqueProducts,customers)

def updateData():
    orderList=Order.objects.values_list('product',flat=True)
    productIds=[x for x in range (1,11)]
    a={1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0}
    for i in orderList:
        a[i]+=1
    print(a)
    return a