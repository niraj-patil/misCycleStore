from django.shortcuts import render


def home(request):
    return render(request,'base.html')

def test(request):
    return render(request,'test.html')

def report():
    pass

def signUp():
    pass

def productPage():
    pass

def paymentPortal():
    pass

def loginPage():
    pass
