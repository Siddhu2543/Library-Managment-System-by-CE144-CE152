from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

urlpatterns = [
    path('home',views.home,name="home"),
    path('add-book',views.addBook,name="addBook"),
    path('view-book/<int:bookid>',views.viewBook,name="viewBook"),
    path('remove-book/<int:bookid>',views.removeBook,name="removeBook"),
    path('update-book/<int:bookid>',views.updateBook,name="updateBook"),
    path('view-user/<int:userid>',views.viewUser,name="viewUser"),
    path('update-user/<int:userid>',views.updateUser,name="updateUser"),
    path('remove-os-book/<int:id>',views.returnBook,name="returnBook"),
    path('notification',views.notification,name="notification"),
    path('approve/<int:id>', views.approve, name="approve"),
    path('deny/<int:id>', views.deny, name="deny")
]