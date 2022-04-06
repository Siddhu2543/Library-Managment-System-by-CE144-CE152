from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

urlpatterns = [
    path('index',views.index,name="index"),
    path('aboutus',views.aboutus,name="aboutus"),
    path('books3sidebar',views.books3sidebar,name="books3sidebar"),
    path('books3sidebar1/<str:cat>',views.books3sidebar1,name="books3sidebar1"),
    path('contactus',views.contactus,name="contactus"),
    path('myprofile',views.myprofile,name="myprofile"),
    path('bookDetails/<int:bookid>',views.bookDetails,name="bookDetails"),
    path('userProfileUpdate',views.userProfileUpdate,name="userProfileUpdate"),
    path('issue-book/<int:bookid>',views.issueBook,name="issueBook"),
    path('reserv-book/<int:bookid>',views.reserveBook,name="reserveBook"),
    path('renew-book/<int:bookid>',views.renewBook,name="renewBook"),
    path('notification',views.notification,name="notification"),
    path('remove-notification/<int:id>',views.removeNotification,name="removeNotification")
]