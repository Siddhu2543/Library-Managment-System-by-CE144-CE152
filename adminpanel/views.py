from asyncio.windows_events import NULL
from multiprocessing import context
from turtle import title
from types import NoneType
from django.contrib import messages
from unicodedata import category
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.db.models import *

from tables.models import Book, Penalty, Profile, Request, Reservation, Transaction

# Create your views here.

@login_required(login_url='/')
def home(request):
    return render(request,'admin.html')

@login_required(login_url='/')
def addBook(request):
    if(request.method == "POST"):
        titel = request.POST['title']
        desc = request.POST['desc']
        author = request.POST['author']
        publishers = request.POST['publishers']
        availableQty = request.POST['availableQty']
        pic = request.FILES.get('pic')
        category = request.POST['category']
    
        if(Book.objects.filter(title=titel).exists()):
            messages.error(request,'Book with the title name already exist!')
        else:
            book = Book(title=titel, description=desc, author=author, publishers=publishers, available_qty=availableQty, book_pic=pic, category=category)
            book.save()
            messages.success(request, "Book Added Successfully...")
            return redirect('/adminpanel/home')

    else:
        return render(request,'add-book.html')

@login_required(login_url='/')
def viewBook(request, bookid):
    book = Book.objects.filter(id=bookid)

    transaction = Transaction.objects.filter(book_id = bookid, current_status = "issued")

    context = {'Book':book, 'tranx': transaction}
    
    return render(request,'books-detail-admin.html',context)

@login_required(login_url='/')
def updateBook(request, bookid):
    if request.method == "POST":
        title = request.POST['title']
        author = request.POST['author']
        desc = request.POST['desc']
        pubs = request.POST['publishers']
        availableQty = request.POST['availableQty']
        cat = request.POST['category']
        pic = request.FILES.get('pic')

        book = Book.objects.get(id = bookid)

        book.title = title
        book.author = author
        book.description = desc
        book.publishers = pubs
        book.available_qty = availableQty
        book.category = cat
        book.book_pic = book.book_pic
        if len(request.FILES) != 0:
            print(1)
            book.book_pic = pic
        
        book.save()

        return redirect("/adminpanel/view-book/"+str(bookid))

    else:
        book = Book.objects.filter(id = bookid)
        context = {'Book': book}
        return render(request,'update-book-details.html', context)

@login_required(login_url='/')
def removeBook(request, bookid):
    book = get_object_or_404(Book, id = bookid)

    book.delete()

    return redirect("/adminpanel/home")

@login_required(login_url='/')
def viewUser(request, userid):
    user = User.objects.filter(id = userid)
    penalties = Penalty.objects.filter(user_id = userid)

    tranx = Transaction.objects.filter(user_id = userid, current_status = 'issued')
    
    issue_cnt = tranx.aggregate(Count('id'))
    penalty_sum = penalties.aggregate(Sum('penalty'))
    reservation_cnt = Reservation.objects.filter(user_id = userid).aggregate(Count('id'))

    context = {'mainuserdetails': user, 'mainpenalties':penalties, 'maintranx': tranx, 'issue_cnt':issue_cnt, 'penalty_sum':penalty_sum, 'reservation_cnt':reservation_cnt}
    return render(request,'view-user-admin.html', context)

@login_required(login_url='/')
def updateUser(request, userid, bookid):
    penalty_remove = get_object_or_404(Penalty, user_id = userid, book_id = bookid)
    penalty_remove.delete()
    return redirect("/adminpanel/view-user"+str(userid))

@login_required(login_url='/')
def returnBook(request, id):
    tranx = get_object_or_404(Transaction, id = id)
    tranx.current_status = 'returned'
    tranx.save()
    book = get_object_or_404(Book, id = tranx.book_id.id)
    book.available_qty += 1
    return redirect("/adminpanel/home")

@login_required(login_url='/')
def notification(request):
    requests = Request.objects.all()
    users = {}
    books = {}
    for r in requests:
        u = get_object_or_404(User, id = r.user_id.id)
        b = get_object_or_404(Book, id = r.book_id.id)
        users.__setitem__(r.user_id.id, u)
        books.__setitem__(r.book_id.id, b)

    context = {'requests': requests, 'users': users, 'books': books}
    return render(request,'notification-admin.html', context)

@login_required(login_url='/')
def approve(request, id):
    req = get_object_or_404(Request, id = id)
    book = get_object_or_404(Book, id = req.book_id.id)
    if req.description == 'issue' and book.available_qty > 0:
        book.available_qty -= 1
        book.save()
        req.admin_status = 1
        req.save()
        tranx = Transaction(user_id = req.user_id, book_id = req.book_id, current_status = 'issued')
        tranx.save()
        p = Penalty(user_id = req.user_id, book_id = req.book_id, penalty=0)
        p.save()
    elif req.description == 'renew':
        req.admin_status = 1
        req.save()
        tranx = get_object_or_404(Transaction, user_id = req.user_id, book_id = req.book_id)
        tranx.current_status = 'renewed'
        tranx.save()
    elif req.description == 'reservation':
        reservation = Reservation(user_id = req.user_id, book_id = req.book_id)
        reservation.save()
    else:
        messages.error(request, 'Request can not be granted')
    return redirect("/adminpanel/notification", messages)

@login_required(login_url='/')
def deny(request, id):
    req = get_object_or_404(Request, id = id)
    req.admin_status = -1
    req.save()
    return redirect("/adminpanel/notification")