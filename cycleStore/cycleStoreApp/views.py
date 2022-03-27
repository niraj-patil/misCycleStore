from urllib import request
from django.shortcuts import render, HttpResponseRedirect
from .forms import FinanceForm
from .reports import *

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
    (profit,total,budgetString,healthString)=fm_report()
    return render(request,'finance/freport.html',{'profit':profit,"total":total,"budgetString":budgetString,"healthString":healthString})

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



def salesMartketingReport():
    ()=sales()
    return render(request,'salesMarketing.html',{})

def signUp():
    pass

def productPage():
    pass

def paymentPortal():
    pass

def loginPage():
    pass
