from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import Indicator
from . import backtesting

def welcome(request):
    return render(request,'welcome.html')

@login_required
def home(request):
    return render(request,'homepage.html')

@login_required
def result(request):
    stock =request.POST["stock"]
    entry = []
    para_entry = []
    value_entry = []
    total_entry = request.POST.get("total_entries")
    for i in range( int(total_entry) ):
        entry.append( request.POST.get("entry"+ str(i+1) ) )
        para_entry.append( request.POST.get("entry_parameter"+ str(i+1) ) )
        value_entry.append( request.POST.get("entry_value"+ str(i+1) ) )
    print(stock)
    print(entry)
    print(para_entry)
    print(value_entry)
    para_exit = []
    value_exit =[]
    exit = []
    total_exit = request.POST.get("total_exits")
    for i in range( int(total_exit) ):
        exit.append( request.POST.get("exit"+ str(i+1) ) )
        para_exit.append( request.POST.get("exit_parameter"+ str(i+1) ) )
        value_exit.append( request.POST.get("exit_value"+ str(i+1) ) )
    print(exit)
    print(para_exit)
    print(value_exit)
    stock = stock[ stock.find('|')+1: ]
    print(stock)
    profit, entry, exit = backtesting.home(stock, entry,para_entry, value_entry, exit, para_exit, value_exit  )
    print(profit)
    print(entry)
    print(exit)
    dict = {}
    if(type(profit) == str):
        dict = {
            "profit": "No match for this strategy"
        }
    else:
        dict = {
            "profit":profit,
            "entry": entry,
            "exit": exit
        }
    return render(request, "result.html", dict)
