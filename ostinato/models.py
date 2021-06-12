from django.db import models
import re
import bcrypt
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name must be at least 2 characters long"

        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name must be at least 2 characters long"

        if len(postData['email']) == 0:
            errors['email'] = "You must enter an email"
        elif not email_regex.match(postData['email']):
            errors['email'] = "Email must be valid"

        all_users = User.objects.filter(email=postData['email'])
        if len(all_users) < 0:
            errors['duplicate'] = "Email is already in use"

        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"

        if postData['password'] != postData['confirm_password']:
            errors['mismatch'] = "Passwords do not match"

        return errors

    def login_validator(self, postData):
        errors={}
        existing_user = User.objects.filter(email=postData['email'])
        if len(postData['email']) == 0:
            errors['email'] = "Email Must Be Entered"
        if len(postData['password']) < 8:
            errors['password'] = "Password is 8 Characters or more"
        elif bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()) != True:
            errors['password'] = "Email and Password do not match"
        return errors

    def edit_validator(self,postData):
        errors={}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name must be at least 2 characters long"
        if len(postData['last_name']) < 2:
            errors['first_name'] = "Last Name must be at least 2 characters long"
        if not email_regex.match(postData['email']):
            errors['email'] = "Invalid Email Address"
        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()

class Post(models.Model):
    message = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, related_name='user_post', on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name='liked_posts')
    album = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)

class Comment(models.Model):
    comment = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    user = models.ForeignKey(User, related_name='files', on_delete=models.CASCADE)