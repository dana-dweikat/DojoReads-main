from django.db import models



class Authors(models.Model):
    name = models.CharField(max_length=125)
    
    def __str__(self) -> str:
        return self.name


#this for validation
class BooksManger(models.Manager):
    def validate(self, post_data):
        errors = {}
        if len(post_data['description']) < 5:
            errors['description'] = 'Description should be at least 5 charters'
        return errors
    
class Books(models.Model):
    author = models.ForeignKey(Authors, on_delete=models.CASCADE)
    title= models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    objects = BooksManger()
    
    def __str__(self):
        return str(self.title)




#this for validation
class UsersManger(models.Manager):
    def validate(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First name should be at least 2 charters'
        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last name should be at least 2 charters'    
        if len(post_data['password1']) < 8:
            errors['password1'] = 'Password should be at least 8 charters'
        return errors


class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email= models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UsersManger()


    def __str__(self):
        return str({self.first_name,self.last_name,self.email})

class Reviews(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    review=models.TextField() 
    stars = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.book.title)
    
    def get_blank_stars_count(self):
        return 5 - self.stars
