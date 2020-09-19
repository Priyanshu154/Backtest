from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def welcome(request):
    return render(request,'welcome.html')

@login_required
def home(request):
    return render(request,'homepage.html')

@login_required
def result(request):
    '''
    stock =request.GET["stock"]
    entry1=request.GET["entry_indicator1"]
    entry2=request.GET["entry_indicator2"]
    exit1=request.GET["exit_indicator1"]
    exit2=request.GET["exit_indicator2"]'''

    return render(request,'result.html',{'stock':stock,'entry1':entry1,'entry2':entry2,'exit1':exit1,'exit2':exit2,})
