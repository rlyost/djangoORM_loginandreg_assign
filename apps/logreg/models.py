from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def log_validator(self, postData):
        errors = {}
        log_email = postData['logemail']
        log_check = User.objects.filter(email=log_email)
        # Validates email address for proper format.
        if len(log_email) < 1:
            errors["email"] = "Email cannot be blank!"
            return errors
        elif not EMAIL_REGEX.match(log_email):
            errors["email"] = "Invalid Email Address!"
            return errors
        elif len(log_check) == 0:
            errors["email"] = "Email not found!"
            return errors
        log_pass = User.objects.get(email=log_email).password
        #password validation - compares hashed logged in password to hashed Db password
        if not bcrypt.checkpw(postData['logpassword'].encode(), log_pass.encode()):
            errors["email"] = "Password does not match."
            return errors
    def reg_validator(self, postData):
        errors = {}
        #grabs record if email exists in the Db
        reg_check = User.objects.filter(email=postData['regemail'])
        # Checks name fields
        if len(postData['fname']) < 2 or len(postData['lname']) < 2:
            errors["name"] = "Name must be longer."
            return errors
        elif not str(postData['fname']).isalpha():
            errors["name"] = "First Name can only be letters."
            return errors       
        elif not str(postData['lname']).isalpha():
            errors["name"] = "Last Name can only be letters."
            return errors
        # Validates email address for proper format.
        if len(postData['regemail']) < 1:
            errors["email"] = "Email cannot be blank!"
            return errors
        elif not EMAIL_REGEX.match(postData['regemail']):
            errors["email"] = "Invalid Email Address!"
            return errors
        elif len(reg_check) != 0:
            errors["email"] = "Duplicate address, please enter another one or try logging in!"
            return errors
        # Check password length and matching confirmation
        if len(postData['regpassword']) < 8:
            errors["password"] = "Password is not long enough!"
            return errors
        elif postData['regpassword'] != postData['regpassword2']:
            errors["password"] = "Passwords do not match!"
            return errors
    
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, default='')
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()