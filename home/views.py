from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/')
def index(request):
    return render(request,'index.html')

@login_required(login_url='/')
def aboutus(request):
    return render(request,'about-us.html')

@login_required(login_url='/')
def books3sidebar(request):
    return render(request,'books3-sidebar.html')

@login_required(login_url='/')
def contactus(request):
    return render(request,'contact-us.html')