from django.shortcuts import render

def Home(request):
    return render(request,'homepage.html')
