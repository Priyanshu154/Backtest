from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def welcome(request):
    return render(request,'welcome.html')

@login_required
def home(request):
    return render(request,'homepage.html')

@login_required
def result(request):
    stock =request.GET["stock"]
    entry = []
    para = []
    value = []
    total_entry = request.GET.get("total_entries")
    for i in range( int(total_entry) ):
        entry.append( request.GET.get("entry"+ str(i+1) ) )
        para.append( request.GET.get("entry_parameter"+ str(i+1) ) )
        value.append( request.GET.get("entry_value"+ str(i+1) ) )
    print(stock)
    print(entry)
    print(para)
    print(value)
    para = []
    value =[]
    exit = []
    total_exit = request.GET.get("total_exits")
    for i in range( int(total_exit) ):
        exit.append( request.GET.get("exit"+ str(i+1) ) )
        para.append( request.GET.get("exit_parameter"+ str(i+1) ) )
        value.append( request.GET.get("exit_value"+ str(i+1) ) )
    print(exit)
    print(para)
    print(value)
    '''
    entry2=request.GET["entry_indicator2"]
    exit1=request.GET["exit_indicator1"]
    exit2=request.GET["exit_indicator2"]
    '''
    return render(request, "homepage.html")
#    return render(request,'result.html',{'stock':stock,'entry1':entry1,'entry2':entry2,'exit1':exit1,'exit2':exit2,})
