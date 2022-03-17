from asyncio.windows_events import NULL
import uuid
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from tables.models import Profile

from django.conf import settings
from django.core.mail import send_mail
import datetime

# Create your views here.
def login(request):
    if(request.method == "POST"):
        uname = request.POST['uname']
        password = request.POST['password']
        
        user = auth.authenticate(username=uname,password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect("index")
        else:
            messages.error(request,'Username or password may be incorrect')
            return HttpResponseRedirect('/')
    else:
        return render(request,'login.html')

def register(request):
    if(request.method == "POST"):
        uname = request.POST['uname']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        fname = request.POST['fname']
        lname = request.POST['lname']
        mobile = request.POST['mobile']
        gen = request.POST['gen']
        branch = request.POST['branch']
        semester = request.POST['semester']
        address = request.POST['address']
        dob = request.POST['dob']
        pic = request.POST['pic']
        if( password == cpassword ):
            
            if(User.objects.filter(username=uname).exists()):
                messages.error(request,'Username is not available')
                return HttpResponseRedirect('register')
            elif(User.objects.filter(email=email).exists()):
                messages.error(request,'Email is already taken')
                return HttpResponseRedirect('register')
            else:
                user=User.objects.create_user(username=uname,password=password,email=email,first_name=fname,last_name=lname)
                profile = Profile(user=user,mobile = mobile,dob=dob,gender=gen,branch=branch,profile_pic=pic,address=address,semester=semester)
                profile.save()
                messages.success(request,'User created successfully...')
                return HttpResponseRedirect('/')
        else:
            messages.error(request,'Password not matching...')
            return HttpResponseRedirect('register')
            
    return render(request,'register.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')