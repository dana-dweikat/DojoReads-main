from django.contrib import admin
from django.urls import path
from . import views 

app_name = 'app1'

urlpatterns = [
    path('', views.registration, name='registration'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('books', views.books_home, name='books_home'),
    path('books/add', views.books_add, name='books_add'),
    path('books/add_new', views.add_new_book, name='add_new_book'),
    path('books/<int:pk>', views.books_num, name='books_num'),
    path('users/<int:pk>', views.users_num, name='users_num'),
    path('add_review', views.add_review, name='add_review'),
    path('delete_review/<int:pk>', views.delete_review,  name='delete_review'),
]
