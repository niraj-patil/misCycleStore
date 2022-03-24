
from ast import Starred
from audioop import add
from .models import *
from datetime import datetime
from calendar import monthrange
from numpy import unique
from django.db.models import Sum

#TODO: Genralize Functions. Set Default Dates to RandomOldestDate and timestamp.now()
def mode(items):
    return max(set(items), key = items.count)
def median(items):
    #items.sort()                               Assumed we send sorted elements
    mid = len(items) // 2                       #Floor Division
    return (items[mid] + items[~mid]) / 2
def mostSoldItemGeneral():
    mostSoldProduct=Product.objects.all().order_by('sales')[0]
    mostSoldProductTypes=UniqueProduct.objects.all().filter(product=mostSoldProduct).order_by('-sales')
    return (mostSoldProduct,mostSoldProductTypes)

def mostSoldItemDetailed():
    mostSoldProductTypes=UniqueProduct.objects.all().order_by('-sales')[0]
    return mostSoldProductTypes

def mostProfitableItem():
    sales=UniqueProduct.objects.values_list('sales',flat=True)
    profitPerItem=UniqueProduct.objects.values_list('product',flat=True)

def mostBusyDay(timeStamps):
    days=[]
    for date in timeStamps:
        days.append(date.strftime('%A'))         #returns weekday
    return mode(days)
def mostBusyTime(timeStamps):
    time=[]
    for date in timeStamps:
        time.append(date.hour)
    return mode(time)
def mostBusyDate(timeStamps):
    dates=[]
    for _date in timeStamps:
        dates.append(_date.date())
    return mode(dates)

def modalAge():
    return mode(list(Customer.objects.values_list('age',flat=True)))
def medianAge():
    return median(list(Customer.objects.values_list('age',flat=True).order_by('age')))

def sales(orderList):
    numberOfSales=len(orderList)
    return numberOfSales

def getProfit(startDate,endDate):
    productList=list(Order.objects.filter(timestamp__date__range=(startDate, endDate)).values_list('product',flat=True))
    profitList=[]
    individualUniqueProfitList=[0]*UniqueProduct.objects.all().count()
    individualProfitList=[0]*Product.objects.all().count()
    for product in productList:
        temp=list(UniqueProduct.objects.filter(id=product).values_list('profitPerItem',flat=True))[0]
        pid=list(UniqueProduct.objects.filter(id=product).values_list('product',flat=True))[0]
        profitList.append(temp)
        individualProfitList[pid-1]=individualProfitList[pid-1]+temp
        individualUniqueProfitList[product-1]=individualUniqueProfitList[product-1]+temp
    overallProfit=sum(profitList)
    return (overallProfit,individualProfitList,individualUniqueProfitList)

def sm_report(startDate=datetime(2000,1,1),endDate=datetime.now()):
    orderList=Order.objects.all().filter(timestamp__date__range=(startDate, endDate))
    timeStamps=list(Order.objects.filter(timestamp__date__range=(startDate, endDate)).values_list('timestamp',flat=True))
    buyerIds=list(Order.objects.filter(timestamp__date__range=(startDate, endDate)).values_list('customer',flat=True))
    buyerAge=list(Customer.objects.filter(ID__in=buyerIds).values_list('age',flat=True))
    buyerGender=list(Customer.objects.filter(ID__in=buyerIds).values_list('gender',flat=True))
    buyerCity=list(Address.objects.filter(id__in=buyerIds).values_list('city',flat=True))
    buyerPincode=list(Address.objects.filter(id__in=buyerIds).values_list('postal_code',flat=True))
    newCustomerAge=list(Customer.objects.filter(timestamp__date__range=(startDate, endDate)).values_list('age',flat=True))
    newCustomerGender=list(Customer.objects.filter(timestamp__date__range=(startDate, endDate)).values_list('gender',flat=True))
    newCustomerAddressIDs=list(Customer.objects.filter(timestamp__date__range=(startDate, endDate)).values_list('billingAddress',flat=True))
    newCustomerCity=list(Address.objects.filter(id__in=newCustomerAddressIDs).values_list('city',flat=True))
    newCustomerPincode=list(Address.objects.filter(id__in=newCustomerAddressIDs).values_list('postal_code',flat=True))
    (overallProfit,individualProfitList,individualUniqueProfitList)=getProfit(startDate,endDate)
    print(individualProfitList)
    _numberOfSales=sales(orderList)
    _mostBusyDay=mostBusyDay(timeStamps)
    _mostBusyTime=mostBusyTime(timeStamps)
    _mostBusyDate=mostBusyDate(timeStamps)
    _modalBuyerAge=mode(buyerAge)
    _modalBuyerGender=mode(buyerGender)
    _modalBuyerCity=mode(buyerCity)
    _modalBuyerPinCode=mode(buyerPincode)
    _modalNewCustomerAge=mode(newCustomerAge)
    _modalNewCustomerGender=mode(newCustomerGender)
    _modalNewCustomerCity=mode(newCustomerCity)
    _modalNewCustomerPinCode=mode(newCustomerPincode)
    return (_numberOfSales,_mostBusyDay,_mostBusyTime,_mostBusyDate,_modalBuyerAge,_modalBuyerGender,_modalBuyerCity,_modalBuyerPinCode,_modalNewCustomerAge,_modalNewCustomerGender,_modalNewCustomerCity,_modalNewCustomerPinCode)

def sm_dailyReport(date=datetime.now()):
    return sm_report(date,date)
def sm_monthlyReport(month,year):
    return sm_report(datetime(year, month, 1),datetime(year, month, monthrange(year,month)[1]))
def sm_annualReport(year):
    return sm_report(datetime(year, 1, 1),datetime(year, 12, 31))

def sm_product(productList,colourList,typeList,startDate=datetime(2000,1,1),endDate=datetime.now()):
    pass
def sm_productDailyReport(productList,colourList,typeList):
    return sm_report(productList,colourList,typeList,datetime.now(),datetime.now())
def sm_productMonthlyReport(productList,colourList,typeList,month,year):
    return sm_report(productList,colourList,typeList,datetime(year, month, 1),datetime(year, month, 31))
def sm_productAnnualReport(productList,colourList,typeList,year):
    return sm_report(productList,colourList,typeList,datetime(year, 1, 1),datetime(year, 12, 31))




def fm_report():
    unpaidEmployees=list(Employee.objects.filter(paid=False).values_list("salary",flat=True))
    # debits=list(Finances.objects.filter(type='-',completed=True).values_list('amount',flat=True))
    credit=sum(list(Finances.objects.filter(type='+',completed=True).values_list('amount',flat=True)))
    # finances=sum(credits)-sum(debits)

    target=Finances.objects.filter(description='target').aggregate(Sum('amount'))['amount__sum']
    budget=Finances.objects.filter(description='budget').aggregate(Sum('amount'))['amount__sum']
    finances=list(Finances.objects.filter(type__in=['+','-'],completed=True).values_list('amount',flat=True))
    (profit,x,y)=getProfit(datetime(datetime.now().year,datetime.now().month,1),datetime.now())
    total=profit+sum(finances)-sum(unpaidEmployees)
    dailyNeed=target/monthrange(datetime.now().year,datetime.now().month)[1]
    budgetString=""
    currentNeed=dailyNeed*datetime.now().day
    total=float(total)
    currentNeed=float(currentNeed)
    health=str(int(total-currentNeed))
    if total>target:
        healthString="Target Reached.Surplus="+health
    elif total>currentNeed+10*dailyNeed:
        healthString="Great. Target in Sight. Surplus="+health
    elif total>currentNeed+5*dailyNeed:
        healthString="Good. Target can be easily reached at this pace. Surplus="+health
    elif total>=currentNeed:
        healthString="OK. On Track. Surplus="+health
    elif total<currentNeed+5*dailyNeed:
        healthString="Bad. Need to Catch Up with the Daily Quota. Deficiet="+health
    else:
        healthString="Dier. Need to take Drastic Steps. Deficiet="+health

    dailySpent=budget/monthrange(datetime.now().year,datetime.now().month)[1]
    currentSpent=dailySpent*datetime.now().day
    budgetHealth=str(int(currentSpent-credit))
    if currentSpent>credit+credit*0.25:
        budgetString="Under The Budget. Surplus="+budgetHealth
    elif currentSpent>=credit:
        budgetString="On Budget. Surplus="+budgetHealth
    elif currentSpent<credit:
        budgetString="Over Spending. Deficiet="+budgetHealth
    return(profit,total,budgetString,healthString)


def lo_report_t1():
    orders=list(Order.objects.all().filter(timestamp__date__range=(datetime(datetime.now().year,datetime.now().month,1),datetime.now())))
    inProcessing=list(Order.objects.all().filter(timestamp__date__range=(datetime(datetime.now().year,datetime.now().month,1),datetime.now())).filter(status='processing'))
    inShipping=list(Order.objects.all().filter(timestamp__date__range=(datetime(datetime.now().year,datetime.now().month,1),datetime.now())).filter(status__in=['shipped','shipment']))
    individualRequirement=[0]*UniqueProduct.objects.all().count()
    individualRequirement=[0]*UniqueProduct.objects.all().count()
    mostBuyersFrom=[0]*UniqueProduct.objects.all().count()
    stockLeft=[0]*UniqueProduct.objects.all().count()
    for order in inProcessing:
        product=order.product.id
        individualRequirement[product-1]+=1
    for i in range(UniqueProduct.objects.all().count()):
        address=list(Order.objects.all().filter(timestamp__date__range=(datetime(datetime.now().year,datetime.now().month,1),datetime.now())).filter(product=UniqueProduct.objects.get(id=i+1)).values_list('shippingAddress',flat=True))
        print(address)
        city=[Address.objects.get(id=x).city for x in address]
        if(len(city)!=0):
            mostBuyersFrom[i]=mode(city)
        else:
            mostBuyersFrom[i]=0
        lastMonthTrend=[0]*UniqueProduct.objects.all().count()
    currentStock=list(UniqueProduct.objects.all().values_list('quantity',flat=True))
    
    print(mostBuyersFrom)
    return inProcessing

def lo_report_t1():
    inShipping=list(Order.objects.all().filter(timestamp__date__range=(datetime(datetime.now().year,datetime.now().month,1),datetime.now())).filter(status__in=['shipped','shipment']))
    individualRequirement=[0]*UniqueProduct.objects.all().count()
    individualRequirement=[0]*UniqueProduct.objects.all().count()
    mostBuyersFrom=[0]*UniqueProduct.objects.all().count()
    stockLeft=[0]*UniqueProduct.objects.all().count()
    for order in inProcessing:
        product=order.product.id
        individualRequirement[product-1]+=1
    for i in range(UniqueProduct.objects.all().count()):
        address=list(Order.objects.all().filter(timestamp__date__range=(datetime(datetime.now().year,datetime.now().month,1),datetime.now())).filter(product=UniqueProduct.objects.get(id=i+1)).values_list('shippingAddress',flat=True))
        print(address)
        city=[Address.objects.get(id=x).city for x in address]
        if(len(city)!=0):
            mostBuyersFrom[i]=mode(city)
        else:
            mostBuyersFrom[i]=0
        lastMonthTrend=[0]*UniqueProduct.objects.all().count()
    currentStock=list(UniqueProduct.objects.all().values_list('quantity',flat=True))
    
    print(mostBuyersFrom)
    return inProcessing


    """
    how many orders currently in processing
        do we have stock
    where are most orders being shipped to
        mode(city) - mode(pin)      : Currently
        mode(city) - mode(pin)      : Overall

    if inventory-len(salesPastMonth)> someValue:
        overstocked
    elif < someAnotherValue:
        understocked(how many more to order)
    else
        optimal stock
    """

"""
overall sm_report
-----------------------
    overall sales   
most product sold
most profitable
    modal age
    modal address
    most busy date
    most busy day
    most busy time

daily/monthly/annual sm_report
------------------------
    sales
most product sold
most profitable
    modal age
    average age
    modal address
    most busy date(not for daily)
    most busy day
    most busy time

    new customers added
    where from
    average age of newly added

product sm_report
-------------------------------------------------
modal/avg customers attribs for that product
age
address
profit
sales
most sales on date
most profitable version
    
modal/avg...(detailed) each unique prodct
    age address...

"""