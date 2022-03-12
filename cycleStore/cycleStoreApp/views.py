from urllib import request
from django.shortcuts import render

from .reports import *

def home(request):
    return render(request,'home.html')

def test(request):
    #outputList=addData()
    #outputList=Customer.objects.values_list('timestamp', flat=True)
    print(sm_report())
    outputList=[1,3]
    return render(request,'test.html',{'outputList':outputList})

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
