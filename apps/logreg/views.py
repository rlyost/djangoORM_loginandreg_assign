from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from time import gmtime, strftime
from .models import *
from django.core import serializers
import json
import bcrypt

# HOME *************************************************

def index(request):
    return render(request, 'logreg/index.html')

# REGISTRATION *************************************************

def registration(request):
    if request.method == "POST":
        #hashes password for storage to the Db        
        hashed_password = bcrypt.hashpw(request.POST['regpassword'].encode(), bcrypt.gensalt(13))
        request.session['name'] = request.POST['name']
        errors = User.objects.reg_validator(request.POST)
        if errors != None:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            request.session['from'] = 0
            #creates a new validated record in database for new user
            user = User.objects.create(name=request.session['name'], user_name=request.POST['user_name'], password=hashed_password, hired_at=request.POST['hired_at'])
            #sets logged in user for use later
            request.session['id'] = user.id
            request.session['from'] = 0
            #redirects to success to display sucessful login
            return redirect('dash')

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
            user = User.objects.get(user_name=request.POST['user_name'])
            request.session['id'] = user.id
            #sets First name for user interaction
            request.session['name'] = user.name
            #sets login or registration indicator
            request.session['from'] = 1
            #redirects to success to display sucessful login
            return redirect('dash')

# FACEBOARD *************************************************

def dash(request):
    this_user = User.objects.get(id=request.session['id'])
    context = {
        'user': this_user,
        'posts': Post.objects.all(),
    }
    return render(request, 'logreg/dash.html', context)

# ADD ITEM TO DATABASE AND POST *************************************************

def add(request):
    if request.method == "POST":
        errors = User.objects.post_validator(request.POST)
        if errors is not None:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('add')
        else:
            userid = request.session['id']
            Post.objects.create(post=request.POST['post'], user_id=userid)
            this_user = User.objects.get(id=request.session['id'])
            context = {
                'user': this_user,
                'posts': Post.objects.all(),
            }
            return render(request, 'logreg/posts_dash.html', context)

def all_json(request):
    posts = Post.objects.all()
    return HttpResponse(serializers.serialize("json", posts), content_type='application/json')

def all_html(request):
    return render(request, 'logreg/posts_dash.html', { "posts": Post.objects.all() })

# DELETE WISH LIST ITEM FROM DATABASE *************************************************

def delete(request, id):
    destroyit = Post.objects.get(id=id)
    destroyit.delete()
    return redirect('dash')

# LOG USER OFF SYSTEM *************************************************

def logoff(request):
    request.session['id'] = 0
    request.session['name'] = ''
    return redirect('/')
