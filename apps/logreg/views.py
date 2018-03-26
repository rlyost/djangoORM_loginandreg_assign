from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from time import gmtime, strftime
from .models import *    
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

# WISHLIST DASHBOARD *************************************************

def dash(request):
    this_user = User.objects.get(id=request.session['id'])
    context = {
        'user': this_user,
        'myitems': Item.objects.filter(users=this_user.id),
        'otheritems': Item.objects.exclude(users=this_user.id),
    }
    return render(request, 'logreg/dash.html', context)

# ADD NEW ITEM *************************************************

def add(request):
    return render(request, 'logreg/add.html')

# DISPLAY WISH LIST ITEM *************************************************

def wish(request, id):
    context = {
        'item': Item.objects.get(id=id),
        'users': User.objects.filter(wishlist=id),
    }
    return render(request, 'logreg/wish.html', context)

# ADD ITEM TO USERS WISH LIST *************************************************

def addmywish(request, id):
    userid = request.session['id']
    addwish = Item.objects.get(id=id)
    addwish.users.add(userid)
    addwish.save()
    return redirect('dash')

# ADD ITEM TO DATABASE AND USERS WISH LIST *************************************************

def additem(request):
    if request.method == "POST":
        errors = User.objects.item_validator(request.POST)
        if errors is not None:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('ushow', profile_id)
        else:
            userid = request.session['id']
            a1 = Item.objects.create(item_name=request.POST['item'], user=User.objects.get(id=userid))
            a1.users.add(userid)
            a1.save()
            return redirect('dash')

# REMOVE ITEM FROM USERS WISH LIST *************************************************

def remove(request, id):
    userid = request.session['id']
    this_user = User.objects.get(id=userid)
    this_item = Item.objects.get(id=id)
    this_item.users.remove(this_user)
    return redirect('dash')

# DELETE WISH LIST ITEM FROM DATABASE *************************************************

def delete(request, id):
    destroyit = Item.objects.get(id=id)
    destroyit.delete()
    return redirect('dash')

# LOG USER OFF SYSTEM *************************************************

def logoff(request):
    request.session['id'] = 0
    request.session['name'] = ''
    return redirect('/')
