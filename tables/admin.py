import imp
from django.contrib import admin

# Register your models here.
from tables.models import *

admin.site.register(Profile)
admin.site.register(Book)
admin.site.register(Transaction)
admin.site.register(Reservation)
admin.site.register(Penalty)
admin.site.register(Request)
