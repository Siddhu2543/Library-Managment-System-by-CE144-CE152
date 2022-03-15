from operator import mod
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta

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

    sem = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8)
    )

    gender = models.CharField(max_length=1, choices=gen)
    branch = models.CharField(max_length=3, choices=brch)
    semester = models.IntegerField(choices=sem)
    profile_pic = models.ImageField(upload_to = 'images/')
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
    description = models.TextField()
    author = models.CharField(max_length=20)
    publishers = models.CharField(max_length=50)
    available_qty = models.IntegerField(default=1)
    book_pic = models.ImageField(upload_to = 'images/')

def one_month():
    return datetime.today() + timedelta(days=30)

class Transaction(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(default= one_month)
    status = (
        ('iss', 'issued'),
        ('ret', 'returned'),
        ('ren', 'renewed'),
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

