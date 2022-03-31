from urllib import request
from django.shortcuts import render, HttpResponseRedirect
from .forms import FinanceForm
from .reports import *
from django.db.models import Sum,Count
from django.db.models.functions import TruncMonth

def home(request):
    return render(request,'home.html')

def test(request):
    #outputList=addData()
    #outputList=Customer.objects.values_list('timestamp', flat=True)
    print(sm_report())
    outputList=[1,3]
    return render(request,'test.html',{'outputList':outputList})


def loReport(request):
    (productNames,currentStock,currentStockDays,getStockBy,lastMonthTrend,mostBuyersFrom,status)=lo_report_t1()
    (ids,productNames2,addressList,postalCodes)=lo_report_t2()
    return render(request,'logistics.html',{'productNames':productNames,'currentStock':currentStock,'currentStockDays':currentStockDays,'getStockBy':getStockBy,'lastMonthTrend':lastMonthTrend,'mostBuyersFrom':mostBuyersFrom,'status':status,'ids':ids,'productNames2':productNames2,'addressList':addressList,'postalCodes':postalCodes})

def fnaReport(request):
    (budget,target,debits,credits,profit,total,budgetString,healthString)=fm_report()
    return render(request,'finance/freport.html',{'budget':budget,'target':target,'debits':debits,'credits':credits,'profit':profit,"total":total,"budgetString":budgetString,"healthString":healthString})

def add_show(request):
    if request.method=='POST':
        fm=FinanceForm(request.POST)
        if fm.is_valid():
            nd=fm.cleaned_data['description']
            nt=fm.cleaned_data['type']
            na=fm.cleaned_data['amount']
            nc=fm.cleaned_data['completed']
            reg=Finances(description=nd,type=nt,amount=na,completed=nc)
            reg.save()
    else:
        fm=FinanceForm()
    fin=Finances.objects.all()

    return render(request,'finance/addandshow.html',{'form':fm,'fin':fin})
    
def update_data(request,id):
    if request.method=='POST':
        pi=Finances.objects.get(pk=id)
        fm=FinanceForm(request.POST,instance=pi)
        if fm.is_valid():
            fm.save()
    else:
        pi=Finances.objects.get(pk=id)
        fm=FinanceForm(instance=pi)
    return render(request,'finance/update.html',{'form':fm})

def delete_data(request,id):
    if request.method=='POST':
        pi=Finances.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/fna')



def salesMartketingReport(request):
    (numberOfSales,overallProfit,mostProfitableProduct,mostProfitableProductUnique,mostBusyDay,mostBusyTime,mostBusyDate,modalBuyerAge,modalBuyerGender,modalBuyerCity,modalBuyerPinCode,modalNewCustomerAge,modalNewCustomerGender,modalNewCustomerCity,modalNewCustomerPinCode)=sm_report()
    
    (dnumberOfSales,doverallProfit,dmostProfitableProduct,dmostProfitableProductUnique,dmostBusyDay,dmostBusyTime,dmostBusyDate,dmodalBuyerAge,dmodalBuyerGender,dmodalBuyerCity,dmodalBuyerPinCode,dmodalNewCustomerAge,dmodalNewCustomerGender,dmodalNewCustomerCity,dmodalNewCustomerPinCode)=sm_dailyReport()
    (ynumberOfSales,yoverallProfit,ymostProfitableProduct,ymostProfitableProductUnique,ymostBusyDay,ymostBusyTime,ymostBusyDate,ymodalBuyerAge,ymodalBuyerGender,ymodalBuyerCity,ymodalBuyerPinCode,ymodalNewCustomerAge,ymodalNewCustomerGender,ymodalNewCustomerCity,ymodalNewCustomerPinCode)=sm_annualReport()
    (mnumberOfSales,moverallProfit,mmostProfitableProduct,mmostProfitableProductUnique,mmostBusyDay,mmostBusyTime,mmostBusyDate,mmodalBuyerAge,mmodalBuyerGender,mmodalBuyerCity,mmodalBuyerPinCode,mmodalNewCustomerAge,mmodalNewCustomerGender,mmodalNewCustomerCity,mmodalNewCustomerPinCode)=sm_monthlyReport()
    
    
    return render(request,'sales/salesMarketing.html',locals())

def dashboard(request):
    _product = request.POST.get('product',1)
    _colour = request.POST.get('colour',1)
    _type= request.POST.get('type',1)
    print(_product,_colour,_type)
    products=Product.objects.all()
    _list=list(Order.objects.annotate(month=TruncMonth('timestamp')).values('month').annotate(total=Count('ID')))
    months=[x['month'].strftime("%B")+" "+str(x['month'].year) for x in _list]
    sales=[x['total'] for x in _list]
    return render(request,'dashboard_with_pivot.html',{'products':products,'months':months,'sales':sales})

def signUp():
    pass

def productPage():
    pass

def paymentPortal():
    pass

def loginPage():
    pass
