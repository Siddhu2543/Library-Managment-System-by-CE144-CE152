from asyncio.windows_events import NULL
import imp
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
import django.core.files.uploadedfile
import datetime
import os

# Create your views here.
def login(request):
    if(request.method == "POST"):
        uname = request.POST['uname']
        password = request.POST['password']
        
        user = auth.authenticate(username=uname,password=password)
        
        if user is not None:
            auth.login(request,user)
            if user.is_superuser == True:
                return redirect("adminpanel/home")
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
        pic = "images/avtar.png"
        
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

def update(request):
    if(request.method == "POST"):
        uname = request.POST['uname']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        mobile = request.POST['mobile']
        gen = request.POST['gen']
        branch = request.POST['branch']
        semester = request.POST['semester']
        address = request.POST['address']
        dob = request.POST['dob']
        current_user = request.user

        if( current_user.username != uname and User.objects.filter(username=uname).exists()):
            messages.error(request,'Username is not available')
            return HttpResponseRedirect('userProfileUpdate')
        elif( current_user.email != email and User.objects.filter(email=email).exists()):
            messages.error(request,'Email is already taken')
            return HttpResponseRedirect('userProfileUpdate')
        else:
            user = User.objects.get(username=current_user.username)
            profile = Profile.objects.get(user_id=user.id)
            
            user.username = uname
            user.email = email
            user.first_name = fname
            user.last_name = lname
            profile.mobile = mobile
            profile.gender = gen
            profile.branch = branch
            profile.semester = semester
            profile.address = address
            profile.dob = dob
            
            user.save()
            profile.save()
            
            # messages.success(request,'User updated successfully...')
            return HttpResponseRedirect('myprofile')
    else:
        return render(request,'userProfileUpdate.html')

def updatePic(request):
    if(request.method == "POST"):
        
        current_user = request.user
        user = User.objects.get(username=current_user.username)
        profile = Profile.objects.get(user_id=user.id)
        
        media_root = settings.MEDIA_ROOT
        path = os.path.join(media_root,profile.profile_pic.name)
        
        if 'pic' in request.FILES:
            if profile.profile_pic.name != "images/avtar.png":
                if(os.path.exists(path)):
                    os.remove(path)
                    profile.profile_pic = request.FILES['pic']
            profile.profile_pic = request.FILES['pic']
        
        user.save()
        profile.save()
        
        return HttpResponseRedirect('myprofile')
    else:
        return render(request,'userProfile.html')


def removePic(request):
    if(request.method == "POST"):
        
        current_user = request.user
        user = User.objects.get(username=current_user.username)
        profile = Profile.objects.get(user_id=user.id)
        
        media_root = settings.MEDIA_ROOT
        path = os.path.join(media_root,profile.profile_pic.name)
        
        if profile.profile_pic.name != "images/avtar.png":
            if(os.path.exists(path)):
                os.remove(path)
                profile.profile_pic = "images/avtar.png"

        user.save()
        profile.save()
        
        return HttpResponseRedirect('myprofile')
    
    else:
        return render(request,'userProfile.html')