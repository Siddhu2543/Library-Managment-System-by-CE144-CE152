from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

urlpatterns = [
    path('index',views.index,name="index"),
    path('aboutus',views.aboutus,name="aboutus"),
    path('books3sidebar',views.books3sidebar,name="books3sidebar"),
    path('contactus',views.contactus,name="contactus")
]