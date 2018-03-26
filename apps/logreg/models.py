from __future__ import unicode_literals
from django.db import models
import bcrypt

class UserManager(models.Manager):
    def log_validator(self, postData):
        errors = {}
        log_user = postData['user_name']
        log_check = User.objects.filter(user_name=log_user)
        # Validates email address for proper format.
        if len(log_user) < 3:
            errors["user"] = "Username must be 3 characters of more"
            return errors
        elif len(log_check) == 0:
            errors["user"] = "Username not found!"
            return errors
        log_pass = User.objects.get(user_name=log_user).password
        #password validation - compares hashed logged in password to hashed Db password
        if not bcrypt.checkpw(postData['logpassword'].encode(), log_pass.encode()):
            errors["user"] = "Password does not match."
            return errors
    def reg_validator(self, postData):
        errors = {}
        #grabs record if user exists in the Db
        reg_check = User.objects.filter(user_name=postData['user_name'])
        # Checks name fields
        if len(postData['name']) < 3:
            errors["name"] = "Name must be longer."
            return errors
        elif not str(postData['name']).isalpha():
            errors["name"] = "Name can only be letters."
            return errors       
        # Validates username for proper format.
        if len(postData['user_name']) < 3:
            errors["user"] = "Username must be 3 characters of more"
            return errors
        elif len(reg_check) != 0:
            errors["user"] = "Duplicate Username, please enter another one or try logging in!"
            return errors
        # Check password length and matching confirmation
        if len(postData['regpassword']) < 8:
            errors["password"] = "Password is not long enough!"
            return errors
        elif postData['regpassword'] != postData['regpassword2']:
            errors["password"] = "Passwords do not match!"
            return errors
    def item_validator(self, postData):
        errors = {}
        if len(postData['item']) < 4:
            errors["item"] = "Item name must be 4 characters or more."
            return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255, default='')
    password = models.CharField(max_length=255)
    hired_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

class Item(models.Model):
    item_name = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="added_by")
    users = models.ManyToManyField(User, related_name="wishlist")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)