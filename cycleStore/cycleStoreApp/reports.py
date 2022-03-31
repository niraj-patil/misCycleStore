
from math import ceil
from .models import *
from datetime import datetime
from calendar import monthrange
from numpy import unique
from django.db.models import Sum

#TODO: Genralize Functions. Set Default Dates to RandomOldestDate and timestamp.now()
def mode(items):
    if(len(items)==0):
        return 0
    return max(set(items), key = items.count)
def median(items):
    #items.sort()                               Assumed we send sorted elements
    mid = len(items) // 2                       #Floor Division
    return (items[mid] + items[~mid]) / 2


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
    mostProfitableProduct=Product.objects.get(ID=individualProfitList.index(max(individualProfitList))+1)
    mostProfitableProduct=mostProfitableProduct.title
    mostProfitableProductUnique=UniqueProduct.objects.get(id=individualProfitList.index(max(individualProfitList))+1)
    mostProfitableProductUnique=mostProfitableProductUnique.product.title+":"+mostProfitableProductUnique.colour.colour+":"+mostProfitableProductUnique.type.type
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
    return (_numberOfSales,overallProfit,mostProfitableProduct,mostProfitableProductUnique,_mostBusyDay,_mostBusyTime,_mostBusyDate,_modalBuyerAge,_modalBuyerGender,_modalBuyerCity,_modalBuyerPinCode,_modalNewCustomerAge,_modalNewCustomerGender,_modalNewCustomerCity,_modalNewCustomerPinCode)

def sm_dailyReport(date=datetime.now()):
    return sm_report(date,date)
def sm_monthlyReport(month=datetime.now().month,year=datetime.now().year):
    return sm_report(datetime(year, month, 1),datetime(year, month, monthrange(year,month)[1]))
def sm_annualReport(year=datetime.now().year):
    return sm_report(datetime(year, 1, 1),datetime(year, 12, 31))

# def sm_product(productList,colourList,typeList,startDate=datetime(2000,1,1),endDate=datetime.now()):
#     pass
# def sm_productDailyReport(productList,colourList,typeList):
#     return sm_report(productList,colourList,typeList,datetime.now(),datetime.now())
# def sm_productMonthlyReport(productList,colourList,typeList,month,year):
#     return sm_report(productList,colourList,typeList,datetime(year, month, 1),datetime(year, month, 31))
# def sm_productAnnualReport(productList,colourList,typeList,year):
#     return sm_report(productList,colourList,typeList,datetime(year, 1, 1),datetime(year, 12, 31))




def fm_report():
    target=Finances.objects.filter(description='target').aggregate(Sum('amount'))['amount__sum']
    budget=Finances.objects.filter(description='budget').aggregate(Sum('amount'))['amount__sum']
    debits=sum(list(Finances.objects.filter(type='-').values_list('amount',flat=True)))
    credits=sum(list(Finances.objects.filter(type='+').values_list('amount',flat=True)))
    (profit,x,y)=getProfit(datetime(datetime.now().year,datetime.now().month,1),datetime.now())
    total=debits-credits
    print(total)
    dailyNeed=target/monthrange(datetime.now().year,datetime.now().month)[1]
    budgetString=""
    
    currentNeed=dailyNeed*datetime.now().day
    currentNeed=float(currentNeed)
    profit=int(profit)
    health=str(int(profit-currentNeed))
    if profit>target:
        healthString="Target Reached.Surplus="+health
    elif profit>currentNeed+10*dailyNeed:
        healthString="Great. Target in Sight. Surplus="+health
    elif profit>currentNeed+5*dailyNeed:
        healthString="Good. Target can be easily reached at this pace. Surplus="+health
    elif profit>=currentNeed:
        healthString="OK. On Track. Surplus="+health
    elif profit<currentNeed+5*dailyNeed:
        healthString="Bad. Need to Catch Up with the Daily Quota. Deficiet="+health
    else:
        healthString="Dier. Need to take Drastic Steps. Deficiet="+health

    dailySpent=budget/monthrange(datetime.now().year,datetime.now().month)[1]
    currentSpent=dailySpent*datetime.now().day
    budgetHealth=str(int(currentSpent-total))
    if currentSpent>total+total*0.25:
        budgetString="Under The Budget. Surplus="+budgetHealth
    elif currentSpent>=total:
        budgetString="On Budget. Surplus="+budgetHealth
    elif currentSpent<total:
        budgetString="Over Spending. Deficiet="+budgetHealth
    return(budget,target,debits,credits,profit,total,budgetString,healthString)


def lo_report_t1():
    inProcessing=list(Order.objects.all().filter(timestamp__date__range=(datetime(datetime.now().year,datetime.now().month,1),datetime.now())).filter(status='processing'))

    numberOfUniqueProducts=UniqueProduct.objects.all().count()
    productNames=[] #
    currentStock=list(UniqueProduct.objects.all().values_list('quantity',flat=True)) #
    currentStockDays=[0]*numberOfUniqueProducts 
    currentRequirement=[0]*numberOfUniqueProducts #
    getStockBy=["-"]*numberOfUniqueProducts
    mostBuyersFrom=[0]*numberOfUniqueProducts
    status=[0]*numberOfUniqueProducts
   
    lastMonthTrend=[0]*numberOfUniqueProducts
    averagePerDayRequirement=[0]*numberOfUniqueProducts

    #productNames
    for _product in list(UniqueProduct.objects.all()):
        name=_product.product.title+":"+_product.type.type+":"+_product.colour.colour
        productNames.append(name)

    #currentRequirement
    for order in inProcessing:
        product=order.product.id
        currentRequirement[product-1]+=1
    
    #last month trend & currentStockDays
    if(datetime.now().month==1):
        mn= 12  
        yr= datetime.now().year-1
    else: 
        mn= datetime.now().month-1
        yr= datetime.now().year
    for i in range(numberOfUniqueProducts):
        _ordersLM=Order.objects.all().filter(timestamp__date__range=(datetime(yr,mn,1),datetime(yr,mn,monthrange(yr,mn)[1]))).filter(product=UniqueProduct.objects.get(id=i+1))
        for _order in _ordersLM:
            product=_order.product.id
            lastMonthTrend[product-1]+=1
            averagePerDayRequirement[product-1]=lastMonthTrend[product-1]/30
            currentStockDays[product-1]=ceil(currentStock[product-1]/averagePerDayRequirement[product-1])


    #city
    for i in range(numberOfUniqueProducts):
        _orders=Order.objects.all().filter(timestamp__date__range=(datetime(datetime.now().year,datetime.now().month,1),datetime.now())).filter(product=UniqueProduct.objects.get(id=i+1))
        city=[x.shippingAddress.city for x in _orders]
        if(len(city)!=0):
            mostBuyersFrom[i]=mode(city)
        else:
            mostBuyersFrom[i]="-"

    #status
    for i in range(numberOfUniqueProducts):
        if(currentStock[i]>lastMonthTrend[i]+10):
            status[i]="Overstocked"
            getStockBy[i]="-"
        elif(currentStock[i]<lastMonthTrend[i]-3):
            status[i]="Understocked"
            if(currentStockDays[i]-7<0):
                getStockBy[i]="Immidiately"
            else:
                getStockBy[i]=str(currentStockDays[i]-7)+" Days"
        else:
            status[i]="Optimal"
        
        if(currentStock[i]<currentRequirement[i]):
            getStockBy[i]="Immidiately"


    
    return (productNames,currentStock,currentStockDays,getStockBy,lastMonthTrend,mostBuyersFrom,status)

def lo_report_t2():
    inShipping=list(Order.objects.all().filter(timestamp__date__range=(datetime(datetime.now().year,datetime.now().month,1),datetime.now())).filter(status__in=['shipped','shipment']))
    ids=[]
    productNames=[]
    addressList=[]
    postalCodes=[]
    for order in inShipping:
        id=order.ID
        name=order.product.product.title+":"+order.product.type.type+":"+order.product.colour.colour
        address=order.shippingAddress.city
        code=order.shippingAddress.postal_code
        ids.append(id)
        productNames.append(name)
        addressList.append(address)
        postalCodes.append(code)
    return (ids,productNames,addressList,postalCodes)


    """
    how many orders currently in processing
       

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
