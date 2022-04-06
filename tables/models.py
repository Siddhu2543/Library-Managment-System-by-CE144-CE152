import imp
from operator import mod
import os
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta, date
from django.utils.timezone import now

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.BigIntegerField(null=False)
    dob = models.DateField(null=False)
    
    gen = (
        ('m', 'Male'),
        ('f', 'Female')
    )

    brch = (
        ('MH', 'MH'),
        ('CL', 'CL'),
        ('CH', 'CH'),
        ('IC', 'IC'),
        ('IT', 'IT'),
        ('CE', 'CE'),
        ('EC', 'EC'),
        ('FOD', 'FOD'),
        ('FOP', 'FOP')
    )

    gender = models.CharField(max_length=1, choices=gen)
    branch = models.CharField(max_length=3, choices=brch)
    semester = models.IntegerField(default='1')
    profile_pic = models.ImageField(upload_to = 'images')
    address = models.TextField(default="Address not given")
    
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


class Book(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(default="Nothing")
    author = models.CharField(max_length=20)
    publishers = models.CharField(max_length=50)
    available_qty = models.IntegerField(default=1)
    
    cat = (
        ('Technology','Technology'),
        ('Mathematics','Mathematics'),
        ('Language','Language'),
        ('Business Management','Business Management'),
        ('Physics','Physics'),
        ('Chemistry','Chemistry'),
        ('Robotics','Robotics'),
        ('Space and Astronomy','Space and Astronomy')
    )
    add_date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=25, choices=cat,default="Technology")
    book_pic = models.ImageField(upload_to = 'images')

def one_month():
    return datetime.today() + timedelta(days=30)

class Transaction(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(default= one_month)
    status = (
        ('issued', 'issued'),
        ('returned', 'returned'),
        ('renewed', 'renewed'),
    )
    current_status = models.CharField(max_length=8, choices=status)

class Reservation(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    reservation_date = models.DateField(auto_now_add=True)

class Penalty(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    penalty = models.IntegerField()
    entry_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(default= one_month)

class Request(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    description = models.TextField()

    admin_stat = (
        (-1, -1),
        (0, 0),
        (1, 1),
    )

    user_stat = (
        (0, 0),
        (1, 1),
    )

    admin_status = models.IntegerField(choices=admin_stat, default=0)
    user_status = models.IntegerField(choices=user_stat, default=0)