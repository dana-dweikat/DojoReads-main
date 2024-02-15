from django.shortcuts import render,redirect
from .models import Users, Reviews, Authors, Books
from django.contrib import messages
import bcrypt

def registration(request):
    user_id = request.session.get('user_id')
    
    if user_id:
        return redirect('app1:books_home')
    
    return render(request, "registration.html") 


def register(request):
    if request.method == "POST":
        
        errors = Users.objects.validate(request.POST)
        
        # There is some errors
        if len(errors) > 0:
            for error in errors.values():
                messages.error(request, error)
            return redirect('app1:registration')
        
        first_name_form = request.POST['first_name']
        last_name_form = request.POST['last_name']
        email_form = request.POST['email']
        password_form = request.POST['password1']
        confirm_password_form = request.POST['password2']
        
        if password_form == confirm_password_form:
            hash_password = bcrypt.hashpw(password_form.encode(), bcrypt.gensalt()).decode()
            
            new_user =Users.objects.create(
                first_name=first_name_form,
                last_name = last_name_form,
                email=email_form,
                password=hash_password)
            
            
            request.session['user_id'] = new_user.id
            return redirect('app1:books_home')

        # if password didn't match
        else:
            messages.error(request, 'Password not match.')
            return redirect('app1:registration')



def login(request):
    if request.method == "POST":
        email_form = request.POST['email']
        password_form = request.POST['password1']
        
        users = Users.objects.filter(email=email_form)
        
        if len(users) == 0:
            messages.error(request, "Email doesn't exist.")
            return redirect('app1:registration')
        
        if bcrypt.checkpw(password_form.encode(), users.first().password.encode()):
            request.session['user_id'] = users.first().id
            return redirect('app1:books_home')
        # if password is wrong
        else:
            messages.error(request, 'Password not correct.')
            return redirect('app1:registration')



def logout(request):
    request.session.flush()
    return redirect('app1:registration')


def books_home(request):
    user_id = request.session.get('user_id')
    # if user not logged in
    if not user_id:
        return redirect('app1:registration')
    
    user = Users.objects.get(id=user_id)
    
    context={
        'user': user,
        'reviews': Reviews.objects.filter().order_by('-created_at')[:3],
        'books':  Books.objects.all()
    }
    return render(request, 'books_home.html', context)



# books_add
def books_add(request):
    all_authors = Authors.objects.all()
    context = {
        'authors' : all_authors
    }
    return render(request, "books_add.html", context)

def add_new_book(request):
    form_title = request.POST['title']
    # THE AUTHOR  ID SELECTED FROM THE FORM
    form_selected_author_id = request.POST.get('selected_author', None)
    form_new_author = request.POST.get('new_author', None)
    form_review = request.POST['review']
    form_stars = request.POST['stars']
    
    # IF USER ADDED NEW AUTHOR
    if form_new_author:
        # GET THE AUTHOR USING THE ID
        new_author = Authors.objects.create(name=form_new_author)
        book = Books.objects.create(title=form_title, author=new_author)
    # CHECK IF USER SELECTED EXISTING AUTHOR
    else:
        selected_author = Authors.objects.get(id = form_selected_author_id)
        book = Books.objects.create(title=form_title, author=selected_author)
        
    # TO CREATE NEW REVIEW WE SHOULD HAVE (BOOK - USER - REVIEW - STARS)
    
    # WE DON'T HAVE THE USER SO WE SHOULD GET IT 
    user_id = request.session.get('user_id')
    current_user = Users.objects.get(id=user_id)
    
    review = Reviews.objects.create(user=current_user, book=book, review=form_review, stars=int(form_stars))
    
    return redirect('app1:books_num', pk=book.id)




def books_num(request, pk):
    book = Books.objects.get(id=pk)
    reviews_for_book = Reviews.objects.filter(book=book)
    
    user_id = request.session.get('user_id')
    current_user = Users.objects.get(id=user_id)
    
    context = {
        'book': book,
        'reviews': reviews_for_book,
        'user' : current_user
    }
    return render(request,"books_num.html", context)


def add_review(request):
    form_book_id = request.POST['book']
    form_stars = request.POST['stars']
    form_review = request.POST['review']
    
    # TO CREATE NEW REVIEW WE SHOULD HAVE (BOOK - USER - REVIEW - STARS)

    
    book = Books.objects.get(id=form_book_id)
    # WE DON'T HAVE THE USER SO WE SHOULD GET IT 
    user_id = request.session.get('user_id')
    current_user = Users.objects.get(id=user_id)
    
    review = Reviews.objects.create(user=current_user, book=book, review=form_review, stars=int(form_stars))
    
    return redirect('app1:books_num', pk=book.id)
    
def delete_review(request, pk):
    review = Reviews.objects.get(id=pk)
    review.delete()
    return redirect('app1:books_home')


# POST users_num
def users_num(request,pk):
    user_view=Users.objects.get(id=pk)
    user_reviews=Reviews.objects.filter(user=user_view)
    context={
              'user':user_view,
              'reviews':user_reviews
    }

   
    return render(request,"users_num.html",context)







