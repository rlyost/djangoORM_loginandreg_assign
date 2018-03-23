from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from time import gmtime, strftime
from .models import *    
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# HOME *************************************************

def index(request):
    return render(request, 'logreg/index.html')

# REGISTRATION *************************************************

def registration(request):
    if request.method == "POST":
        #hashes password for storage to the Db        
        hashed_password = bcrypt.hashpw(request.POST['regpassword'].encode(), bcrypt.gensalt(13))
        request.session['fname'] = request.POST['fname']
        errors = User.objects.reg_validator(request.POST)
        if errors != None:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            request.session['from'] = 0
            #creates a new validated record in database for new user
            User.objects.create(first_name=request.session['fname'], last_name=request.POST['lname'], email=request.POST['regemail'], password=hashed_password)
            #sets logged in user for use later
            request.session['id'] = User.objects.last().id
            request.session['from'] = 0
            #redirects to success to display sucessful login
            return redirect('usuccess')

# LOGIN *************************************************

def login(request):
    if request.method == "POST":
        errors = User.objects.log_validator(request.POST)
        if errors != None:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            #sets logged in user id for use later  
            request.session['id'] = User.objects.get(email=request.POST['logemail']).id
            #sets First name for user interaction
            request.session['fname'] = User.objects.get(email=request.POST['logemail']).first_name
            #sets login or registration indicator
            request.session['from'] = 1
            #redirects to success to display sucessful login
            return redirect('usuccess')

# SUCCESSFUL LOGIN OR REGISTRATION *************************************************

def success(request):
    if request.session['from'] == 1:
        messages.success(request, "Welcome Back {}!  You have successfully logged in!".format(request.session['fname']))
    else:
        messages.success(request, "Welcome {}!  You have successfully registered on our site!".format(request.session['fname']))
    return render(request, 'logreg/success.html')
