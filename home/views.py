import imp
from multiprocessing import context
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import *

from tables.models import Book, Penalty, Request, Reservation, Transaction

# Create your views here.

@login_required(login_url='/')
def index(request):
    return render(request,'index.html')

@login_required(login_url='/')
def aboutus(request):
    return render(request,'about-us.html')

@login_required(login_url='/')
def books3sidebar(request):
    
    if(request.method == "GET"):
        
        allbooks = Book.objects.all()
        
        context = {'AllBooks':allbooks}
        
        return render(request,'books3-sidebar.html',context)
    
@login_required(login_url='/')
def books3sidebar1(request,cat):
    
    if(request.method == "GET"):
        allbooks = Book.objects.filter(category=cat)
        context = {'AllBooks':allbooks}
            
        return render(request,'books3-sidebar.html',context)
        
        
        

@login_required(login_url='/')
def contactus(request):
    return render(request,'contact-us.html')

@login_required(login_url='/')
def myprofile(request):
    penalties = Penalty.objects.filter(user_id = request.user.id)

    tranx = Transaction.objects.filter(user_id = request.user, current_status = 'issued')
    
    issue_cnt = tranx.aggregate(Count('id'))
    penalty_sum = penalties.aggregate(Sum('penalty'))
    reservation_cnt = Reservation.objects.filter(user_id = request.user).aggregate(Count('id'))

    context = {'mainpenalties':penalties, 'maintranx': tranx, 'issue_cnt':issue_cnt, 'penalty_sum':penalty_sum, 'reservation_cnt':reservation_cnt}
    return render(request,'userProfile.html', context)

@login_required(login_url='/')
def bookDetails(request,bookid):
    
    book = Book.objects.filter(id=bookid)
    flag = -1
    if len(Transaction.objects.filter(book_id = bookid, user_id = request.user.id, current_status = 'issued')) != 0:
        flag = 0
    
    context = {'Book':book, 'flag': flag}
    
    return render(request,'books-detail.html',context)

@login_required(login_url='/')
def userProfileUpdate(request):
    return render(request,'userProfileUpdate.html')

@login_required(login_url='/')
def notification(request):
    req = Request.objects.filter(user_id = request.user.id, user_status = 0).exclude(admin_status = 0)
    books = {}
    for r in req:
        b = get_object_or_404(Book, id = r.book_id.id)
        books.__setitem__(b.id, b)

    context = {'user_notification': req, 'notification_books':books}
    return render(request,'notification.html', context)

@login_required(login_url='/')
def removeNotification(request, id):
    req = get_object_or_404(Request, id = id)
    req.user_status = 1
    req.save()
    return redirect('/notification')

@login_required(login_url='/')
def issueBook(request, bookid):
    book = get_object_or_404(Book, id = bookid)
    req = Request(user_id = request.user, book_id = book, description = 'issue')
    req.save()
    return redirect("/index")

@login_required(login_url='/')
def reserveBook(request, bookid):
    book = get_object_or_404(Book, id = bookid)
    req = Request(user_id = request.user, book_id = book, description = 'reserve')
    req.save()
    return redirect("/index")

@login_required(login_url='/')
def renewBook(request, bookid):
    book = get_object_or_404(Book, id = bookid)
    req = Request(user_id = request.user, book_id = book, description = 'renew')
    req.save()
    return redirect("/index")