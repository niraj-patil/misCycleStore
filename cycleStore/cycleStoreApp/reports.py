from .models import *
from datetime import datetime
from numpy import unique

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
    uniqueProductList=UniqueProduct.objects.values_list(flat=True)
    numberOfSales=sales(orderList)
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
    return (numberOfSales,_mostBusyDay,_mostBusyTime,_mostBusyDate,_modalBuyerAge,_modalBuyerGender,_modalBuyerCity,_modalBuyerPinCode,_modalNewCustomerAge,_modalNewCustomerGender,_modalNewCustomerCity,_modalNewCustomerPinCode)

def sm_product():
    pass

def sm_dailyReport():
    return sm_report(datetime.now(),datetime.now())
def sm_monthlyReport(month,year):
    return sm_report(datetime(year, month, 1),datetime(year, month, 31))
def sm_annualReport(year):
    return sm_report(datetime(year, 1, 1),datetime(year, 12, 31))

def fm_report():
    unpaidEmployees=list(Employee.objects.filter(paid=False).values_list("salary",flat=True))
    finances=list(Finances.objects.filter(type__in=['+','-'],completed=True).values_list('amount',flat=True))
    total=sum(finances)-sum(unpaidEmployees)
    return(total)


def lo_report():
    pass
    """
    how many orders currently in processing
        do we have stock
    how many orders currently been shipped
        mode(city) - mode(pin)      : Current
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
